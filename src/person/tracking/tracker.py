import dlib
import collections
import time
import numpy as np

from src.person.detection.detector import PersonDetector
from src.filter.nms import non_max_suppression_slow
from src.filter.tracker_filter import filter_undetected_trackers
from settings import MARGIN

person_detector = PersonDetector()


def track_persons(trackers, attributes):

    all_track_rects = []
    all_track_keys = []

    for fid in trackers.keys():

        tracked_position = trackers[fid].get_position()
        t_left = int(tracked_position.left())
        t_top = int(tracked_position.top())
        t_right = int(tracked_position.right())
        t_bottom = int(tracked_position.bottom())
        all_track_rects.append([t_left, t_top, t_right, t_bottom])
        all_track_keys.append(fid)

    filter_ids = non_max_suppression_slow(boxes=np.array(all_track_rects), keys=all_track_keys)

    for idx in filter_ids:
        attributes.pop(idx)
        trackers.pop(idx)

    for fid in trackers.keys():

        tracked_position = trackers[fid].get_position()
        t_left = int(tracked_position.left())
        t_top = int(tracked_position.top())
        t_right = int(tracked_position.right())
        t_bottom = int(tracked_position.bottom())

        attributes[fid]["box"] = [t_left, t_top, t_right, t_bottom]
        # cv2.rectangle(person_frame, (int(w_ratio * t_left), int(h_ratio * t_top)),
        #               (int(w_ratio * t_right), int(h_ratio * t_bottom)), (0, 0, 255), 3)
        #
        # cv2.putText(person_frame, "ID:{}".format(str(attributes[fid]["id"])),
        #             (int(w_ratio * t_right), int(h_ratio * t_top)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

    return attributes


def create_person_tracker(detect_img, trackers, attributes, person_id):

    st_time = time.time()
    # person_positions = person_detector.detect_person(frame=img)
    person_positions = person_detector.detect_person_tensorflow(frame=detect_img)
    print(time.time() - st_time)

    detected_centers = []

    for coordinates in person_positions:

        left, top, right, bottom = coordinates
        x_bar = 0.5 * (left + right)
        y_bar = 0.5 * (top + bottom)
        detected_centers.append([left, top, right, bottom])

        matched_fid = None

        for fid in trackers.keys():

            tracked_position = trackers[fid].get_position()
            t_left = int(tracked_position.left())
            t_top = int(tracked_position.top())
            t_right = int(tracked_position.right())
            t_bottom = int(tracked_position.bottom())

            # calculate the center point
            t_x_bar = 0.5 * (t_left + t_right)
            t_y_bar = 0.5 * (t_top + t_bottom)

            # check if the center point of the face is within the rectangle of a tracker region.
            # Also, the center point of the tracker region must be within the region detected as a face.
            # If both of these conditions hold we have a match

            if t_left <= x_bar <= t_right and t_top <= y_bar <= t_bottom and left <= t_x_bar <= right \
                    and top <= t_y_bar <= bottom:
                matched_fid = fid
                trackers.pop(fid)
                tracker = dlib.correlation_tracker()
                tracker.start_track(detect_img, dlib.rectangle(left - MARGIN, top - MARGIN, right + MARGIN,
                                                               bottom + MARGIN))
                trackers[matched_fid] = tracker
                attributes[matched_fid]["undetected"] = 0

                # cv2.rectangle(show_img, (int(w_ratio * t_left), int(h_ratio * t_top)),
                #               (int(w_ratio * t_right), int(h_ratio * t_bottom)), (0, 0, 255), 3)
                #
                # cv2.putText(show_img, "ID:{}".format(str(attributes[matched_fid]["id"])),
                #             (int(w_ratio * t_right), int(h_ratio * t_top)),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
        # If no matched fid, then we have to create a new tracker
        if matched_fid is None:
            print("Creating new tracker " + str(person_id))
            # Create and store the tracker
            tracker = dlib.correlation_tracker()
            tracker.start_track(detect_img, dlib.rectangle(left - MARGIN, top - MARGIN, right + MARGIN,
                                                           bottom + MARGIN))
            trackers[person_id] = tracker

            temp_dict = collections.defaultdict()
            temp_dict["id"] = str(person_id)
            temp_dict["box"] = [left, top, right, bottom]
            temp_dict["undetected"] = 0
            attributes[person_id] = temp_dict
            # cv2.rectangle(show_img, (int(w_ratio * left), int(h_ratio * top)),
            #               (int(w_ratio * right), int(h_ratio * bottom)), (0, 0, 255), 3)
            #
            # cv2.putText(show_img, "ID:{}".format(str(attributes[person_id]["id"])),
            #             (int(w_ratio * right), int(h_ratio * top)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

            # Increase the currentFaceID counter
            person_id += 1

    trackers, attributes = filter_undetected_trackers(trackers=trackers, attributes=attributes,
                                                      detected_rects=detected_centers)

    return trackers, attributes, person_id


if __name__ == '__main__':

    track_persons(trackers={}, attributes={})
