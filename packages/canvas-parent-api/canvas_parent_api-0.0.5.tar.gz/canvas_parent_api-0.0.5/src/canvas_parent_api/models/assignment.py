"""Assignment Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import AssignmentResponse


class Assignment(DataModel):
    """Assignment Model Definition."""
    def __init__(self, assignment_resp: AssignmentResponse):
        self._id = assignment_resp.id
        self._name = assignment_resp.name
        self._description = assignment_resp.description
        self._created_at = assignment_resp.created_at
        self._updated_at = assignment_resp.updated_at
        self._due_at = assignment_resp.due_at
        self._lock_at = assignment_resp.lock_at
        self._unlock_at = assignment_resp.unlock_at
        self._has_overrides = assignment_resp.has_overrides
        self._all_dates = assignment_resp.all_dates
        self._course_id = assignment_resp.course_id
        self._html_url = assignment_resp.html_url
        self._submission_download_url = assignment_resp.submission_download_url
        self._assignment_group_id = assignment_resp.assignment_group_id
        self._due_date_required = assignment_resp.due_date_required
        self._allowed_extensions = assignment_resp.allowed_extensions
        self._max_name_length = assignment_resp.max_name_length
        self._turnitin_enabled = assignment_resp.turnitin_enabled
        self._vericite_enabled = assignment_resp.vericite_enabled
        self._turnitin_settings = assignment_resp.turnitin_settings
        self._grade_group_students_individually = assignment_resp.grade_group_students_individually
        self._external_tool_tag_attributes = assignment_resp.external_tool_tag_attributes
        self._peer_reviews = assignment_resp.peer_reviews
        self._automatic_peer_reviews = assignment_resp.automatic_peer_reviews
        self._peer_review_count = assignment_resp.peer_review_count
        self._peer_reviews_assign_at = assignment_resp.peer_reviews_assign_at
        self._intra_group_peer_reviews = assignment_resp.intra_group_peer_reviews
        self._group_category_id = assignment_resp.group_category_id
        self._needs_grading_count = assignment_resp.needs_grading_count
        self._needs_grading_count_by_section = assignment_resp.needs_grading_count_by_section
        self._position = assignment_resp.position
        self._post_to_sis = assignment_resp.post_to_sis
        self._integration_id = assignment_resp.integration_id
        self._integration_data = assignment_resp.integration_data
        self._points_possible = assignment_resp.points_possible
        self._submission_types = assignment_resp.submission_types
        self._has_submitted_submissions = assignment_resp.has_submitted_submissions
        self._grading_type = assignment_resp.grading_type
        self._grading_standard_id = assignment_resp.grading_standard_id
        self._published = assignment_resp.published
        self._unpublishable = assignment_resp.unpublishable
        self._only_visible_to_overrides = assignment_resp.only_visible_to_overrides
        self._locked_for_user = assignment_resp.locked_for_user
        self._locked_info = assignment_resp.locked_info
        self._lock_explanation = assignment_resp.lock_explanation
        self._quiz_id = assignment_resp.quiz_id
        self._anonymous_submission = assignment_resp.anonymous_submissions
        self._discussion_topic = assignment_resp.discussion_topic
        self._freeze_on_copy = assignment_resp.freeze_on_copy
        self._frozen = assignment_resp.frozen
        self._frozen_attributes = assignment_resp.frozen_attributes
        self._submission = assignment_resp.submission
        self._use_rubric_for_grading = assignment_resp.use_rubric_for_grading
        self._rubric_settings = assignment_resp.rubric_settings
        self._rubric = assignment_resp.rubric
        self._assignment_visibility = assignment_resp.assignment_visibility
        self._overrides = assignment_resp.overrides
        self._omit_from_final_grade = assignment_resp.omit_from_final_grade
        self._moderated_grading = assignment_resp.moderated_grading
        self._grader_count = assignment_resp.grader_count
        self._final_grader_id = assignment_resp.final_grader_id
        self._grader_comments_visible_to_graders = assignment_resp.grader_comments_visible_to_graders
        self._graders_anonymous_to_graders = assignment_resp.graders_anonymous_to_graders
        self._grader_names_visible_to_final_grader = assignment_resp.grader_names_visible_to_final_grader
        self._anonymous_grading = assignment_resp.anonymous_grading
        self._post_manually = assignment_resp.post_manually
        self._score_statistics = assignment_resp.score_statistics
        self._can_submit = assignment_resp.can_submit
        self._annotatable_attachment_id = assignment_resp.annotatable_attachment_id
        self._anonymize_students = assignment_resp.anonymize_students
        self._require_lockdown_browser = assignment_resp.require_lockdown_browser
        self._important_dates = assignment_resp.important_dates
        self._muted = assignment_resp.muted

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> str:
        """Property Definition."""
        return self._name

    @property
    def description(self) -> str:
        """Property Definition."""
        return self._description

    @property
    def created_at(self) -> str:
        """Property Definition."""
        return self._created_at

    @property
    def updated_at(self) -> str:
        """Property Definition."""
        return self._updated_at

    @property
    def due_at(self) -> str:
        """Property Definition."""
        return self._due_at

    @property
    def lock_at(self) -> str:
        """Property Definition."""
        return self._lock_at

    @property
    def unlock_at(self) -> str:
        """Property Definition."""
        return self._unlock_at

    @property
    def has_overrides(self) -> bool:
        """Property Definition."""
        return self._has_overrides

    @property
    def all_dates(self) -> list:
        """Property Definition."""
        return self._all_dates

    @property
    def course_id(self) -> int:
        """Property Definition."""
        return self._course_id

    @property
    def html_url(self) -> str:
        """Property Definition."""
        return self._html_url

    @property
    def submission_download_url(self) -> str:
        """Property Definition."""
        return self._submission_download_url

    @property
    def assignment_group_id(self) -> int:
        """Property Definition."""
        return self._assignment_group_id

    @property
    def due_date_required(self) -> bool:
        """Property Definition."""
        return self._due_date_required

    @property
    def allowed_extensions(self) -> list:
        """Property Definition."""
        return self._allowed_extensions

    @property
    def max_name_length(self) -> int:
        """Property Definition."""
        return self._max_name_length

    @property
    def turnitin_enabled(self) -> bool:
        """Property Definition."""
        return self._turnitin_enabled

    @property
    def vericite_enabled(self) -> bool:
        """Property Definition."""
        return self._vericite_enabled

    @property
    def turnitin_settings(self) -> dict:
        """Property Definition."""
        return self._turnitin_settings

    @property
    def grade_group_students_individually(self) -> bool:
        """Property Definition."""
        return self._grade_group_students_individually

    @property
    def external_tool_tag_attributes(self) -> dict:
        """Property Definition."""
        return self._external_tool_tag_attributes

    @property
    def peer_reviews(self) -> bool:
        """Property Definition."""
        return self._peer_reviews

    @property
    def automatic_peer_reviews(self) -> bool:
        """Property Definition."""
        return self._automatic_peer_reviews

    @property
    def peer_review_count(self) -> int:
        """Property Definition."""
        return self._peer_review_count

    @property
    def peer_reviews_assign_at(self) -> str:
        """Property Definition."""
        return self._peer_reviews_assign_at

    @property
    def intra_group_peer_reviews(self) -> bool:
        """Property Definition."""
        return self._intra_group_peer_reviews

    @property
    def group_category_id(self) -> int:
        """Property Definition."""
        return self._group_category_id

    @property
    def needs_grading_count(self) -> int:
        """Property Definition."""
        return self._needs_grading_count

    @property
    def needs_grading_count_by_section(self) -> list:
        """Property Definition."""
        return self._needs_grading_count_by_section

    @property
    def position(self) -> int:
        """Property Definition."""
        return self._position

    @property
    def post_to_sis(self) -> bool:
        """Property Definition."""
        return self._post_to_sis

    @property
    def integration_id(self) -> str:
        """Property Definition."""
        return self._integration_id

    @property
    def integration_data(self) -> dict:
        """Property Definition."""
        return self._integration_data

    @property
    def points_possible(self) -> float:
        """Property Definition."""
        return self._points_possible

    @property
    def submission_types(self) -> list:
        """Property Definition."""
        return self._submission_types

    @property
    def has_submitted_submissions(self) -> bool:
        """Property Definition."""
        return self._has_submitted_submissions

    @property
    def grading_type(self) -> str:
        """Property Definition."""
        return self._grading_type

    @property
    def grading_standard_id(self) -> bool:
        """Property Definition."""
        return self._grading_standard_id

    @property
    def published(self) -> bool:
        """Property Definition."""
        return self._published

    @property
    def unpublishable(self) -> bool:
        """Property Definition."""
        return self._unpublishable

    @property
    def only_visible_to_overrides(self) -> bool:
        """Property Definition."""
        return self._only_visible_to_overrides

    @property
    def locked_for_user(self) -> bool:
        """Property Definition."""
        return self._locked_for_user

    @property
    def locked_info(self) -> str:
        """Property Definition."""
        return self._locked_info

    @property
    def lock_explanation(self) -> str:
        """Property Definition."""
        return self._lock_explanation

    @property
    def quiz_id(self) -> int:
        """Property Definition."""
        return self._quiz_id

    @property
    def anonymous_submissions(self) -> bool:
        """Property Definition."""
        return self._anonymous_submission

    @property
    def discussion_topic(self) -> dict:
        """Property Definition."""
        return self._discussion_topic

    @property
    def freeze_on_copy(self) -> bool:
        """Property Definition."""
        return self._freeze_on_copy

    @property
    def frozen(self) -> bool:
        """Property Definition."""
        return self._frozen

    @property
    def frozen_attributes(self) -> list:
        """Property Definition."""
        return self._frozen_attributes

    @property
    def submission(self) -> dict:
        """Property Definition."""
        return self._submission

    @property
    def use_rubric_for_grading(self) -> bool:
        """Property Definition."""
        return self._use_rubric_for_grading

    @property
    def rubric_settings(self) -> dict:
        """Property Definition."""
        return self._rubric_settings

    @property
    def rubric(self) -> list:
        """Property Definition."""
        return self._rubric

    @property
    def assignment_visibility(self) -> list:
        """Property Definition."""
        return self._assignment_visibility

    @property
    def overrides(self) -> list:
        """Property Definition."""
        return self._overrides

    @property
    def omit_from_final_grade(self) -> bool:
        """Property Definition."""
        return self._omit_from_final_grade

    @property
    def moderated_grading(self) -> bool:
        """Property Definition."""
        return self._moderated_grading

    @property
    def grader_count(self) -> int:
        """Property Definition."""
        return self._grader_count

    @property
    def final_grader_id(self) -> int:
        """Property Definition."""
        return self._final_grader_id

    @property
    def grader_comments_visible_to_graders(self) -> bool:
        """Property Definition."""
        return self._grader_comments_visible_to_graders

    @property
    def graders_anonymous_to_graders(self) -> bool:
        """Property Definition."""
        return self._graders_anonymous_to_graders

    @property
    def grader_names_visible_to_final_grader(self) -> bool:
        """Property Definition."""
        return self._grader_names_visible_to_final_grader

    @property
    def anonymous_grading(self) -> bool:
        """Property Definition."""
        return self._anonymous_grading

    @property
    def post_manually(self) -> bool:
        """Property Definition."""
        return self._post_manually

    @property
    def score_statistics(self) -> list:
        """Property Definition."""
        return self._score_statistics

    @property
    def can_submit(self) -> bool:
        """Property Definition."""
        return self._can_submit

    @property
    def annotatable_attachment_id(self) -> bool:
        """Property Definition."""
        return self._annotatable_attachment_id

    @property
    def anonymize_students(self) -> bool:
        """Property Definition."""
        return self._anonymize_students

    @property
    def require_lockdown_browser(self) -> bool:
        """Property Definition."""
        return self._require_lockdown_browser

    @property
    def important_dates(self) -> bool:
        """Property Definition."""
        return self._important_dates

    @property
    def muted(self) -> bool:
        """Property Definition."""
        return self._muted
