"""Course Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import CourseResponse


class Course(DataModel):
    """Define Course Model."""
    def __init__(self, course_resp: CourseResponse):
        self._id = course_resp.id
        self._sis_course_id = course_resp.sis_course_id
        self._uuid = course_resp.uuid
        self._integration_id = course_resp.integration_id
        self._sis_import_id = course_resp.sis_import_id
        self._name = course_resp.name
        self._course_code = course_resp.course_code
        self._original_name = course_resp.original_name
        self._workflow_state = course_resp.workflow_state
        self._account_id = course_resp.account_id
        self._root_account_id = course_resp.root_account_id
        self._enrollment_term_id = course_resp.enrollment_term_id
        self._grading_periods = course_resp.grading_periods
        self._grading_standard_id = course_resp.grading_standard_id
        self._grade_passback_setting = course_resp.grade_passback_setting
        self._created_at = course_resp.created_at
        self._start_at = course_resp.start_at
        self._end_at = course_resp.end_at
        self._locale = course_resp.locale
        self._enrollments = course_resp.enrollments
        self._total_students = course_resp.total_students
        self._calendar = course_resp.calendar
        self._default_view = course_resp.default_view
        self._syllabus_body = course_resp.syllabus_body
        self._needs_grading_count = course_resp.needs_grading_count
        self._term = course_resp.term
        self._course_progress = course_resp.course_progress
        self._apply_assignment_group_weights = course_resp.apply_assignment_group_weights
        self._permissions = course_resp.permissions
        self._is_public = course_resp.is_public
        self._is_public_to_auth_users = course_resp.is_public_to_auth_users
        self._public_syllabus = course_resp.public_syllabus
        self._public_syllabus_to_auth = course_resp.public_syllabus_to_auth
        self._public_description = course_resp.public_description
        self._storage_quota_mb = course_resp.storage_quota_mb
        self._storage_quota_used_mb = course_resp.storage_quota_used_mb
        self._hide_final_grades = course_resp.hide_final_grades
        self._license = course_resp.license
        self._allow_student_assignment_edits = course_resp.allow_student_assignment_edits
        self._allow_wiki_comments = course_resp.allow_wiki_comments
        self._allow_student_forum_attachments = course_resp.allow_student_forum_attachments
        self._open_enrollment = course_resp.open_enrollment
        self._self_enrollment = course_resp.self_enrollment
        self._restrict_enrollments_to_course_dates = \
            course_resp.restrict_enrollments_to_course_dates
        self._course_format = course_resp.course_format
        self._access_restricted_by_date = course_resp.access_restricted_by_date
        self._time_zone = course_resp.time_zone
        self._blueprint = course_resp.blueprint
        self._blueprint_restrictions = course_resp.blueprint_restrictions
        self._blueprint_restrictions_by_object_type = \
            course_resp.blueprint_restrictions_by_object_type
        self._template = course_resp.template

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def sis_course_id(self) -> int:
        """Property Definition."""
        return self._sis_course_id

    @property
    def uuid(self) -> str:
        """Property Definition."""
        return self._uuid

    @property
    def integration_id(self) -> int:
        """Property Definition."""
        return self._integration_id

    @property
    def sis_import_id(self) -> int:
        """Property Definition."""
        return self._sis_import_id

    @property
    def name(self) -> str:
        """Property Definition."""
        return self._name

    @property
    def course_code(self) -> str:
        """Property Definition."""
        return self._course_code

    @property
    def original_name(self) -> str:
        """Property Definition."""
        return self._original_name

    @property
    def workflow_state(self) -> str:
        """Property Definition."""
        return self._workflow_state

    @property
    def account_id(self) -> int:
        """Property Definition."""
        return self._account_id

    @property
    def root_account_id(self) -> int:
        """Property Definition."""
        return self._root_account_id

    @property
    def enrollment_term_id(self) -> int:
        """Property Definition."""
        return self._enrollment_term_id

    @property
    def grading_periods(self) -> list[int]:
        """Property Definition."""
        return self._grading_periods

    @property
    def grading_standard_id(self) -> int:
        """Property Definition."""
        return self._grading_standard_id

    @property
    def grade_passback_setting(self) -> str:
        """Property Definition."""
        return self._grade_passback_setting

    @property
    def created_at(self) -> str:
        """Property Definition."""
        return self._created_at

    @property
    def start_at(self) -> str:
        """Property Definition."""
        return self._start_at

    @property
    def end_at(self) -> str:
        """Property Definition."""
        return self._end_at

    @property
    def locale(self) -> str:
        """Property Definition."""
        return self._locale

    @property
    def enrollments(self) -> list:
        """Property Definition."""
        return self._enrollments

    @property
    def total_students(self) -> int:
        """Property Definition."""
        return self._total_students

    @property
    def calendar(self) -> dict:
        """Property Definition."""
        return self._calendar

    @property
    def default_view(self) -> str:
        """Property Definition."""
        return self._default_view

    @property
    def syllabus_body(self) -> str:
        """Property Definition."""
        return self._syllabus_body

    @property
    def needs_grading_count(self) -> int:
        """Property Definition."""
        return self._needs_grading_count

    @property
    def term(self) -> dict:
        """Property Definition."""
        return self._term

    @property
    def course_progress(self) -> int:
        """Property Definition."""
        return self._course_progress

    @property
    def apply_assignment_group_weights(self) -> bool:
        """Property Definition."""
        return self._apply_assignment_group_weights

    @property
    def permissions(self) -> dict[any, any]:
        """Property Definition."""
        return self._permissions

    @property
    def is_public(self) -> bool:
        """Property Definition."""
        return self._is_public

    @property
    def is_public_to_auth_users(self) -> bool:
        """Property Definition."""
        return self._is_public_to_auth_users

    @property
    def public_syllabus(self) -> bool:
        """Property Definition."""
        return self._public_syllabus

    @property
    def public_syllabus_to_auth(self) -> bool:
        """Property Definition."""
        return self._public_syllabus_to_auth

    @property
    def public_description(self) -> str:
        """Property Definition."""
        return self._public_description

    @property
    def storage_quota_mb(self) -> int:
        """Property Definition."""
        return self._storage_quota_mb

    @property
    def storage_quota_used_mb(self) -> int:
        """Property Definition."""
        return self._storage_quota_used_mb

    @property
    def hide_final_grades(self) -> bool:
        """Property Definition."""
        return self._hide_final_grades

    @property
    def license(self) -> str:
        """Property Definition."""
        return self._license

    @property
    def allow_student_assignment_edits(self) -> bool:
        """Property Definition."""
        return self._allow_student_assignment_edits

    @property
    def allow_wiki_comments(self) -> bool:
        """Property Definition."""
        return self._allow_wiki_comments

    @property
    def allow_student_forum_attachments(self) -> bool:
        """Property Definition."""
        return self._allow_student_forum_attachments

    @property
    def open_enrollment(self) -> bool:
        """Property Definition."""
        return self._open_enrollment

    @property
    def self_enrollment(self) -> bool:
        """Property Definition."""
        return self._self_enrollment

    @property
    def restrict_enrollments_to_course_dates(self) -> bool:
        """Property Definition."""
        return self._restrict_enrollments_to_course_dates

    @property
    def course_format(self) -> str:
        """Property Definition."""
        return self._course_format

    @property
    def access_restricted_by_date(self) -> bool:
        """Property Definition."""
        return self._access_restricted_by_date

    @property
    def time_zone(self) -> str:
        """Property Definition."""
        return self._time_zone

    @property
    def blueprint(self) -> bool:
        """Property Definition."""
        return self._blueprint

    @property
    def blueprint_restrictions(self) -> dict[any, any]:
        """Property Definition."""
        return self._blueprint_restrictions

    @property
    def blueprint_restrictions_by_object_type(self) -> dict[any, any]:
        """Property Definition."""
        return self._blueprint_restrictions_by_object_type

    @property
    def template(self) -> bool:
        """Property Definition."""
        return self._template
