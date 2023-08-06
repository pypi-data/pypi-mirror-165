"""
This class implements a buffer containing a set of states. It will serve as interface with the
individual states.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 16-07-2022
"""

from collections import deque

import numpy as np

from warnings import warn
from vid2info.utils.config import TIME_FORMAT, ELEMENT_AGE_TIME_FORMAT
from vid2info.utils.general import time_as_str, iou
from vid2info.state.config import ELEMENT_BUFFER_SIZE, INITIAL_TIMESTAMP, OUT_TIMESTAMP, INITIAL_CLASS_NAME, \
    OUT_CLASS_NAME, FINITE_STATE_MACHINE, TRACK_LENGTH
from vid2info.state.finite_state_machine.element_finite_state_machine import ElementFiniteStateMachine
from vid2info.state.config import BUFFER_SIZE
from vid2info.state.scene_state import SceneState
from vid2info.state.element_state import ElementState
from time import time

class StateBuffer:
    def __init__(self, buffer_size : int = BUFFER_SIZE, running_online = False,
                 scene_state_class : callable = SceneState, element_state_class : callable = ElementState,
                 finite_state_machines_config: dict | None = None, keep_elements_history: bool = False):
        """
        Initialize the StateBuffer. It is used for tracking the history of the last scene and
         element states.

        :param buffer_size: int. The size of the history buffer to keep.
        :param running_online: bool. If True, it will assume that the video is comming from an online stream
                like a webcam. So the timestamps of the states will update with the current time in every call.
                If False, it will assume that the video is coming from a pre-recorded file. So the timestamps
                will have to be served from the video.
        :param scene_state_class: type. The class of the scene state. It should be a subclass of SceneState.
        :param element_state_class: Class. The class of the element states. It should be a subclass of ElementState.
        :param finite_state_machines_config: dict. The configuration of the finite state machines for the elements.
                It is a dictionary with the track_id as key and the configuration as value.
        :param keep_elements_history: bool. If True, the element states will be kept in the buffer. If False, the
                element states will be removed from the buffer when they are not in the scene anymore.
        """
        self.buffer_size = max(buffer_size, 1)
        self.buffer = deque(maxlen=self.buffer_size)
        self.running_online = running_online
        self.scene_state_class = scene_state_class
        self.element_state_class = element_state_class
        self.finite_state_machines_config = finite_state_machines_config
        self.keep_elements_history = keep_elements_history
        self.elements_history = {}

        self.recovered_tracks_correspondences = {}

    def state_from_tracker_out(self, tracker_out : dict, add_to_buffer : bool = True,
                               frame: np.ndarray | None = None,
                               segmentation_mask : dict | None = None) -> SceneState:
        """
        Create a new state from the tracker output.

        :param tracker_out: dictionary. The output of the tracker. It is the dictionary outputted by
                get_track_ids when return_as_dict is True. It's keys are the track_ids and the values are
                dictionaries with, at least, the following keys: ('bbox_xyxy', 'confidence', 'class_id', 'track_length')
        :param add_to_buffer: bool. If True, the state will be added to the buffer.
        :param frame: np.ndarray or None. The frame of the scene. If given, it will save a cropped subimage for
                each detected element.
        :param segmentation_mask: np.ndarray or None. The segmentation mask of the scene. If given, it will save a
                cropped segmentation mask for each detected element.
        :return: SceneState. The new state. If add_to_buffer was True it can be also found in the last element of the
                current self.buffer.
        """
        scene_state = self.scene_state_class(tracker_out=tracker_out,
                           get_first_element_time_stamp=self.get_first_element_time_stamp,
                           frame=frame, segmentation_mask=segmentation_mask,
                           element_state_class=self.element_state_class, buffer=self,
                           element_state_machine_configs=self.finite_state_machines_config)
        if add_to_buffer:
            self.buffer.append(scene_state)
            self.update_history(scene_state)
        return scene_state


    def get_first_element_time_stamp(self, track_id : int) -> float | None:
        """
        Get the first_timestamp of the first detection of the element with the given track_id in the buffer
        or None if the element is not in the buffer.

        Args:
            track_id: int. The track_id of the element to get the first_timestamp of.
        """
        for scene_state in self.buffer:
            if track_id in scene_state.elements:
                return scene_state.elements[track_id].first_detection_timestamp
        if self.running_online:
            return time()
        else:
            raise NotImplementedError("Not implemented yet for the case where the video is not coming from an online stream.")


    def get_last_detection_of_element(self, track_id: int) -> ElementState | None:
        """
        Get the last detection of the element with the given track_id in the buffer or None if
        the element is not in the buffer.

        :param track_id: int. The track_id of the element to get the last detection of.
        """
        for scene_state in reversed(self.buffer):
            if track_id in scene_state.elements:
                return scene_state.elements[track_id]
        return None

    def get_biggest_bbox_of_element(self, track_id: int, bboxes_to_past = 10) -> np.ndarray | None:
        """
        Gets the biggest bbox of the element with the given track_id in the buffer or None if the element is
         not in the buffer.

        :param track_id: int. The track_id of the element to get the biggest bbox of.
        :param bboxes_to_past: int. The number of bboxes to look back in the buffer.
        """
        biggest_area, biggest_bbox, checked_bboxes = -1, None, 0
        for scene_state in reversed(self.buffer[-frames_to_past:]):
            if track_id in scene_state.elements:
                bbox = scene_state.elements[track_id].bbox_xyxy
                area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                if area > biggest_area:
                    biggest_area = area
                    biggest_bbox = bbox
                checked_bboxes += 1
            if checked_bboxes >= bboxes_to_past:
                break
        return biggest_bbox

    def get_element_buffer(self, track_id: int, buffer_size: int = ELEMENT_BUFFER_SIZE) -> deque:
        """
        Returns a buffer with the last buffer_size elements with the given track_id in the scene_buffer. If the track_id
        disappears in the scene_buffer for some in between frames, these frames will be ignored. So the buffer will be
        not representative of the distance between frames.

        :param track_id: int. The track_id of the element we want to get the buffer for.
        :param buffer_size: int. The maximum size of the expected buffer.

        :return deque. A buffer containing the last buffer_size elements with the given track_id in the scene_buffer.
        """
        element_buffer = deque(maxlen=buffer_size)
        # Read the scene_buffer backwards
        for scene_state in reversed(self.buffer):
            if track_id in scene_state.elements:
                element_buffer.append(scene_state.elements[track_id])
            if len(element_buffer) == buffer_size:
                break
        element_buffer = deque(reversed(element_buffer))
        return element_buffer

    def get_element_state_machine(self, track_id: int, current_class: str | None = None, bbox_xyxy: np.ndarray | None = None,
                                  recover_default_machines: bool = True, in_scene_tracks: tuple | list = ()) -> ElementFiniteStateMachine:
        """
        Returns the state machine of the element with the given track_id. If this element is new,
        it will create a new state machine using the configs given in element_state_machine_configs.

        :param track_id: int. The track_id of the element.
        :param current_class : str | None. The current class of the element, only used if the element is new.
        :param bbox_xyxy: np.ndarray | None. The bounding box of the element, only used if the element is new.
        :param recover_default_machines: bool. If True, the default state machines will be recovered if the element is new.
        :param in_scene_tracks: tuple | list. The tracks of the elements that are actually in the scene. Only used if
                recover_default_machines is True.

        :return ElementFiniteStateMachine. The current state machine of the element.
        """
        # Check for the last aparition of the element in the buffer.
        last_detection = self.get_last_detection_of_element(track_id=track_id)
        if last_detection is not None:
            finite_state_machine = last_detection.finite_state_machine
        else:
            assert current_class is not None, "If the element is new, the current class must be given."
            if current_class not in self.finite_state_machines_config:
                assert 'default' in self.finite_state_machines_config, f"Element class {current_class} not found " \
                                                                       f"in finite state machine configs and no default " \
                                                                       f"config found."
                if recover_default_machines:
                    recovered_track_id = self.recover_track_id(new_track_id=track_id, class_name=current_class,
                                                               bbox_xyxy=bbox_xyxy, in_scene_tracks=in_scene_tracks)
                    if recovered_track_id is not None:
                        self.recovered_tracks_correspondences[track_id] = recovered_track_id
                        return self.get_element_state_machine(track_id=recovered_track_id, current_class=current_class,
                                                               recover_default_machines=False)

                warn(f"Element class {current_class} not found in finite state machine configs. Using default")
                current_class = 'default'
            config = self.finite_state_machines_config[current_class]
            finite_state_machine = ElementFiniteStateMachine(config=config)
        return finite_state_machine

    def recover_track_id(self, new_track_id: int, class_name: str, bbox_xyxy: np.ndarray,
                         max_time_difference_in_seconds: float | int = 20.0,
                         in_scene_tracks : list | tuple = ()) -> int | None:
        """
        Tries to recover the track_id of an element for which we suspect that the track_id could have been lost
        given its finite_state_machine. If the track_id is recovered, it will be returned. If not, None will be returned.

        NOTE: This is only reliable when the elements are very static. Do not relay in this function if your elements
        are moving and tends to be overlapping between them.

        :param new_track_id: int. The track_id of the element for which we suspect that the original track_id could
                                have been lost.
        :param class_name: str. The current class detected for that element.
        :param bbox_xyxy: np.ndarray. The current bounding box of the element.
        :param max_time_difference_in_seconds: float | int. The maximum time difference in seconds to consider than
                                                an element in the history has not checked.

        :return int | None. The track_id of the element if it is recovered, None otherwise.
        """
        # TODO: It could be improved by checking that the same element does not correspond to other tracks in the same
        #  scene
        current_time = time()
        # Search in the elements_history for those elements that have the same out_class_name than our current class.
        suspicious_track_ids = []
        for track_id, element_info in self.elements_history.items():
            # If the class is the same as the output class of the element and the time difference is short enough
            if track_id not in in_scene_tracks and element_info[OUT_CLASS_NAME] == class_name and \
                    element_info[OUT_TIMESTAMP] > current_time - max_time_difference_in_seconds:
                # Consider it as suspicious
                suspicious_track_ids.append(track_id)
        if len(suspicious_track_ids) > 0:
            # Check for the closer bbox to the current bbox
            suspicious_bboxes = [self.get_biggest_bbox_of_element(track_id=suspicious_track_id)
                                 for suspicious_track_id in suspicious_track_ids]
            # Get the intersection over union (IoU) between the current bbox and each suspicious bbox
            iou_values = [iou(bbox_xyxy, suspicious_bbox) for suspicious_bbox in suspicious_bboxes]
            # Get the index of the biggest IoU value
            max_iou_index = np.argmax(iou_values)
            old_track_id = suspicious_track_ids[max_iou_index]
            return old_track_id

        return None



    def update_history(self, state : SceneState):
        """
        Update the elements_history dictionary. It will keep the track of all the elements that have been
        seen during the analysis.
        """
        for track_id, element in state.elements.items():
            if track_id not in self.elements_history:
                initial_hist_state = {
                    INITIAL_TIMESTAMP: element.first_detection_timestamp,
                    INITIAL_CLASS_NAME: element.class_name,
                    FINITE_STATE_MACHINE: element.finite_state_machine
                }
                self.elements_history[track_id] = initial_hist_state

            element_hist_update = {
                OUT_TIMESTAMP: element.timestamp,
                OUT_CLASS_NAME: element.class_name,
                TRACK_LENGTH: element.track_length
            }
            self.elements_history[track_id].update(element_hist_update)

    def print_elements_history(self, min_track_length: int = 10):
        """
        Print the elements_history dictionary.
        """
        for track_id, element in self.elements_history.items():
            track_len = element[TRACK_LENGTH]
            if track_len > min_track_length:
                start, end = element[INITIAL_TIMESTAMP], element[OUT_TIMESTAMP]
                print("Track id: ", track_id)
                print(f"\t From: {time_as_str(start, time_format=TIME_FORMAT)} - To: {time_as_str(end, time_format=TIME_FORMAT)} "
                      f"(Age: {time_as_str(end - start, time_format=ELEMENT_AGE_TIME_FORMAT)})")
                print(f"\t Entered as: {element[INITIAL_CLASS_NAME]} - Left as: {element[OUT_CLASS_NAME]}")
                print(f"\t Track length: {track_len}")
                print(f"\t Finite state machine: \n{element[FINITE_STATE_MACHINE]}")

