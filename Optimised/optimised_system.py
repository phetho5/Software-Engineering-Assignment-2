class Validator:

    def validate_format(self, data):

        print("SubmissionController -> Validator: validateFormat(data)")

        if data == "":
            print("Validator -> SubmissionController: invalid")
            return False

        print("Validator -> SubmissionController: valid")
        return True


class SubmissionDatabase:

    def save_submission(self, data):

        print("SubmissionController -> SubmissionDatabase: saveSubmission(data)")
        print("SubmissionDatabase -> SubmissionController: submissionId")

        return 101


class ReviewerManager:

    def assign_reviewers(self, submission_id):

        print("SubmissionController -> ReviewerManager: assignReviewers(submissionId)")
        print("ReviewerManager -> SubmissionController: assignedReviewers")

        return ["Reviewer 1", "Reviewer 2", "Reviewer 3"]

    def request_review(self, reviewer, submission_id):

        print(f"ReviewerManager -> {reviewer}: requestReview(submissionId)")
        print(f"{reviewer} -> ReviewerManager: reviewScore")

        return 75


class EvaluationManager:

    def calculate_average(self, scores):

        print("SubmissionController -> EvaluationManager: calculateAverage(submissionId)")
        average = sum(scores) / len(scores)

        print("EvaluationManager -> SubmissionController: averageScore")

        return average

    def check_consensus(self, scores):

        print("SubmissionController -> EvaluationManager: checkConsensus(submissionId)")

        consensus = max(scores) - min(scores) <= 15

        print("EvaluationManager -> SubmissionController: consensusResult")

        return consensus


class DecisionTable:

    def evaluate_decision(self, average, consensus):

        print("SubmissionController -> DecisionTable: evaluateDecision(score, consensus)")

        if average >= 70 and consensus:
            decision = "Accepted"

        elif average < 50:
            decision = "Rejected"

        else:
            decision = "Revision Required"

        print("DecisionTable -> SubmissionController: finalDecision")

        return decision


class NotificationService:

    def send_notification(self, decision):

        if decision == "Accepted":
            print("SubmissionController -> NotificationService: sendAcceptance()")

        elif decision == "Rejected":
            print("SubmissionController -> NotificationService: sendRejection()")

        else:
            print("SubmissionController -> NotificationService: sendRevisionRequest()")

        print(f"NotificationService -> Researcher: final notification ({decision})")


class SubmissionController:

    def __init__(self):

        self.validator = Validator()
        self.database = SubmissionDatabase()
        self.reviewer_manager = ReviewerManager()
        self.evaluation_manager = EvaluationManager()
        self.decision_table = DecisionTable()
        self.notification_service = NotificationService()

    def process_submission(self, data):

        print("Researcher -> UI: uploadSubmission(data)")
        print("UI -> SubmissionController: processSubmission(data)")

        valid = self.validator.validate_format(data)

        if not valid:
            self.notification_service.send_notification("Rejected")
            print("\nFinal Outcome: Rejected")
            return

        submission_id = self.database.save_submission(data)

        reviewers = self.reviewer_manager.assign_reviewers(submission_id)

        scores = []

        for reviewer in reviewers:
            score = self.reviewer_manager.request_review(
                reviewer,
                submission_id
            )
            scores.append(score)

        average = self.evaluation_manager.calculate_average(scores)

        consensus = self.evaluation_manager.check_consensus(scores)

        decision = self.decision_table.evaluate_decision(
            average,
            consensus
        )

        self.notification_service.send_notification(decision)

        print(f"\nFinal Outcome: {decision}")


controller = SubmissionController()
controller.process_submission("Research Paper")
