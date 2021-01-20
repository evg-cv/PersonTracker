import cv2

from src.person.detection.detector import PersonDetector
from src.social_distance.calculator import calculate_real_distance_two_persons
from src.person.tracking.tracker import create_person_tracker, track_persons
from utils.folder_file_manager import log_print
from settings import SAFE_DISTANCE, TRACK_QUALITY, PERSON_TRACK_CYCLE


class SocialDistanceEstimator:

    def __init__(self):
        self.person_detector = PersonDetector()
        self.person_trackers = {}
        self.current_person_id = 1
        self.person_attributes = {}

    def main(self, vid_path=None):

        if vid_path is None:
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(vid_path)
        cnt = 0
        while True:

            ret, frame = cap.read()
            if not ret:
                break
            fids_to_delete = []
            for fid in self.person_trackers.keys():
                tracking_quality = self.person_trackers[fid].update(frame)

                # If the tracking quality is good enough, we must delete this tracker
                if tracking_quality < TRACK_QUALITY:
                    fids_to_delete.append(fid)

            for fid in fids_to_delete:
                print("Removing fid " + str(fid) + " from list of trackers")
                self.person_trackers.pop(fid, None)
                self.person_attributes.pop(fid, None)

            if cnt % PERSON_TRACK_CYCLE == 0:
                self.person_trackers, self.person_attributes, self.current_person_id = \
                    create_person_tracker(detect_img=frame, trackers=self.person_trackers,
                                          attributes=self.person_attributes, person_id=self.current_person_id)
            else:
                self.person_attributes = track_persons(trackers=self.person_trackers, attributes=self.person_attributes)

            cnt += 1
            social_distance_frame = self.estimate_social_distance(frame=frame)
            total_person = len(self.person_trackers.keys())
            cv2.putText(social_distance_frame, "Total : {}".format(total_person),
                        (10, social_distance_frame.shape[0] - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imshow("Social Distance Estimation", social_distance_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()

    def estimate_social_distance(self, frame):

        distance = {}
        for fid_i in self.person_trackers.keys():
            distance["person_{}".format(fid_i)] = {}
            for fid_j in self.person_trackers.keys():
                if fid_i == fid_j:
                    continue
                try:
                    geometry = calculate_real_distance_two_persons(self.person_attributes[fid_i]["box"],
                                                                   self.person_attributes[fid_j]["box"])
                except Exception as e:
                    log_print(info_str=e)
                    geometry = 0
                distance["person_{}".format(fid_i)][fid_j] = geometry

        for fid_i in self.person_trackers.keys():
            left, top, right, bottom = self.person_attributes[fid_i]["box"]
            # text = "person_" + str(fid_i)
            inter_dist = []
            inter_person_id = []
            close_ret = False
            for fid_j in distance["person_{}".format(fid_i)].keys():
                if distance["person_{}".format(fid_i)][fid_j] <= SAFE_DISTANCE:
                    inter_dist.append(distance["person_{}".format(fid_i)][fid_j])
                    inter_person_id.append(fid_j)
                    close_ret = True
            if close_ret:
                # min_dist = min(inter_dist)
                # min_person_id = inter_person_id[inter_dist.index(min_dist)]
                # warning_str = text + ";" + "person_" + str(min_person_id) + ":" + str(min_dist) + "cm"
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # cv2.putText(frame, warning_str, (left, max(top - 10, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                #             (0, 0, 255), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # cv2.putText(frame, text, (left, max(top - 10, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                #             (0, 255, 0), 2)
            cv2.putText(frame, str(fid_i + 1), (left, max(top - 5, 0)), cv2.FONT_HERSHEY_TRIPLEX, 1,
                        (0, 255, 0), 2)

        return frame


if __name__ == '__main__':

    SocialDistanceEstimator().main(vid_path="")
