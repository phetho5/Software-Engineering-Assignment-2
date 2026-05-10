# Task 5: Optimised Implementation

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
        print("SubmissionController -> Validator: validateSubmission(data)")
        validation_result = self.validator.validate_submission(data)

        if not validation_result:
            print("SubmissionController -> NotificationService: sendNotification(Invalid Submission)")
            self.notification_service.send_notification("Invalid Submission")
            return "Invalid Submission"

        print("SubmissionController -> Database: saveSubmission(data)")
        self.database.save_submission(data)

        print("SubmissionController -> ReviewerManager: assignAvailableReviewers(data)")
        assigned_reviewers = self.reviewer_manager.assign_available_reviewers(data)

        print("SubmissionController -> EvaluationManager: evaluateSubmission(data, assignedReviewers)")
        final_outcome = self.evaluation_manager.evaluate_submission(data, assigned_reviewers)

        print("SubmissionController -> NotificationService: sendNotification(finalOutcome)")
        self.notification_service.send_notification(final_outcome)

        return final_outcome


class Validator:
    def validate_submission(self, data):
        return "title" in data and "content" in data


class Database:
    def save_submission(self, data):
        print("Database -> SubmissionController: confirmation")
        return True


class ReviewerManager:
    def assign_available_reviewers(self, data):
        reviewers = [
            Reviewer("Reviewer 1", 75),
            Reviewer("Reviewer 2", 78),
            Reviewer("Reviewer 3", 74)
        ]

        print("ReviewerManager -> SubmissionController: assignedReviewers")
        return reviewers


class Reviewer:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def review_submission(self, data):
        print(f"{self.name} -> EvaluationManager: reviewSubmission(data)")
        return self.score


class EvaluationManager:
    def evaluate_submission(self, data, reviewers):
        scores = []

        for reviewer in reviewers:
            score = reviewer.review_submission(data)
            scores.append(score)

        average_score = sum(scores) / len(scores)
        consensus = max(scores) - min(scores) <= 10

        if average_score >= 70 and consensus:
            return "Accepted"
        elif average_score < 50:
            return "Rejected"
        else:
            return "Revision Required"


class NotificationService:
    def send_notification(self, outcome):
        print(f"NotificationService -> Researcher: notifyResult({outcome})")


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