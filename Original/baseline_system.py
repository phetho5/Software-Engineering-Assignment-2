# Task 1: Baseline Implementation (with sequence-style output)

class Researcher:
    def submit_research_output(self, ui, data):
        print("Researcher -> UI: submitResearchOutput(data)")
        return ui.submit(data)


class UI:
    def __init__(self, submission_controller):
        self.submission_controller = submission_controller

    def submit(self, data):
        print("UI -> SubmissionController: submit(data)")
        return self.submission_controller.submit(data)


class SubmissionController:
    def __init__(self, validator, database, reviewer_manager, evaluation_manager, notification_service):
        self.validator = validator
        self.database = database
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager
        self.notification_service = notification_service

    def submit(self, data):
        print("SubmissionController -> Validator: validateFormat(data)")
        valid_format = self.validator.validate_format(data)

        if not valid_format:
            print("SubmissionController -> UI: return error")
            return "Submission failed: Invalid format"

        print("SubmissionController -> Database: saveSubmission(data)")
        self.database.save_submission(data)

        print("SubmissionController -> ReviewerManager: getAvailableReviewers()")
        reviewers = self.reviewer_manager.get_available_reviewers()

        print("SubmissionController -> ReviewerManager: assignReviewers()")
        assigned_reviewers = self.reviewer_manager.assign_reviewers(reviewers)

        print("SubmissionController -> EvaluationManager: startEvaluation()")
        scores = self.evaluation_manager.start_evaluation(assigned_reviewers, data)

        print("SubmissionController -> EvaluationManager: calculateAverage()")
        average_score = self.evaluation_manager.calculate_average(scores)

        print("SubmissionController -> EvaluationManager: checkConsensus()")
        consensus = self.evaluation_manager.check_consensus(scores)

        print("SubmissionController -> EvaluationManager: applyRules()")
        outcome = self.evaluation_manager.apply_rules(average_score, consensus)

        print("SubmissionController -> NotificationService: sendNotification()")
        self.notification_service.send_notification(outcome)

        return outcome


class Validator:
    def validate_format(self, data):
        print("Validator -> SubmissionController: validateFormat(data)")

        if "title" in data and "content" in data:
            print("Validator -> SubmissionController: valid")
            return True
        else:
            print("Validator -> SubmissionController: invalid")
            return False


class Database:
    def save_submission(self, data):
        print("Database -> SubmissionController: confirmation")
        return True


class ReviewerManager:
    def get_available_reviewers(self):
        print("ReviewerManager -> SubmissionController: reviewerList")

        reviewers = [
            Reviewer("Reviewer 1"),
            Reviewer("Reviewer 2"),
            Reviewer("Reviewer 3")
        ]

        return reviewers

    def assign_reviewers(self, reviewers):
        print("ReviewerManager -> Reviewer: assignReview()")
        return reviewers


class Reviewer:
    def __init__(self, name):
        self.name = name

    def assign_review(self):
        print(f"{self.name} -> System: assignReview()")

    def submit_score(self, data):
        print(f"{self.name} -> EvaluationManager: submitScore()")
        return 75


class EvaluationManager:
    def start_evaluation(self, reviewers, data):
        scores = []

        for reviewer in reviewers:
            reviewer.assign_review()
            score = reviewer.submit_score(data)
            scores.append(score)

        return scores

    def calculate_average(self, scores):
        return sum(scores) / len(scores)

    def check_consensus(self, scores):
        highest = max(scores)
        lowest = min(scores)
        return highest - lowest <= 10

    def apply_rules(self, average_score, consensus):
        if average_score >= 70 and consensus:
            print("EvaluationManager -> SubmissionController: notifyAcceptance()")
            return "Accepted"
        elif average_score < 50:
            print("EvaluationManager -> SubmissionController: notifyRejection()")
            return "Rejected"
        else:
            print("EvaluationManager -> SubmissionController: notifyRevision()")
            return "Revision Required"


class NotificationService:
    def send_notification(self, outcome):
        print(f"NotificationService -> Researcher: sendNotification({outcome})")


# Main execution
if __name__ == "__main__":
    validator = Validator()
    database = Database()
    reviewer_manager = ReviewerManager()
    evaluation_manager = EvaluationManager()
    notification_service = NotificationService()

    submission_controller = SubmissionController(
        validator,
        database,
        reviewer_manager,
        evaluation_manager,
        notification_service
    )

    ui = UI(submission_controller)
    researcher = Researcher()

    submission_data = {
        "title": "Software Engineering Assignment",
        "content": "This is the submitted artefact."
    }

    result = researcher.submit_research_output(ui, submission_data)

    print("\nFinal Outcome:", result)