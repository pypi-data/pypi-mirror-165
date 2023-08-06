"""Base Model Definition."""
from typing import Optional
from pydantic import BaseModel, Field


class ObserveeResponse(BaseModel):
    """Observee Response Definition."""
    id: int
    name: str
    created_at: str
    sortable_name: str
    short_name: str
    observation_link_root_account: Optional[list[int]]


class CourseResponse(BaseModel):
    """Course Response Definition."""
    id: int
    sis_course_id: Optional[int]
    uuid: str
    integration_id: Optional[int]
    sis_import_id: Optional[int]
    name: str
    course_code: str
    original_name: Optional[str]
    workflow_state: str
    account_id: int
    root_account_id: int
    enrollment_term_id: int
    grading_periods: Optional[list]
    grading_standard_id: Optional[int] = Field(...)
    grade_passback_setting: Optional[str] = Field(...)
    created_at: str
    start_at: Optional[str] = Field(...)
    end_at: Optional[str] = Field(...)
    locale: Optional[str]
    enrollments: Optional[list]
    total_students: Optional[int]
    calendar: Optional[dict]
    default_view: str
    syllabus_body: Optional[str]
    needs_grading_count: Optional[int]
    term: Optional[dict]
    course_progress: Optional[int]
    apply_assignment_group_weights: bool
    permissions: Optional[dict]
    is_public: Optional[bool] = Field(...)
    is_public_to_auth_users: bool
    public_syllabus: bool
    public_syllabus_to_auth: bool
    public_description: Optional[str]
    storage_quota_mb: Optional[int]
    storage_quota_used_mb: Optional[int]
    hide_final_grades: Optional[bool]
    license: Optional[str] = Field(...)
    allow_student_assignment_edits: Optional[bool]
    allow_wiki_comments: Optional[bool]
    allow_student_forum_attachments: Optional[bool]
    open_enrollment: Optional[bool]
    self_enrollment: Optional[bool]
    restrict_enrollments_to_course_dates: Optional[bool]
    course_format: Optional[str]
    access_restricted_by_date: Optional[bool]
    time_zone: str
    blueprint: Optional[bool]
    blueprint_restrictions: Optional[dict]
    blueprint_restrictions_by_object_type: Optional[dict]
    template: bool


class AssignmentResponse(BaseModel):
    """Assignment Response Definition"""
    id: int
    name: str
    description: Optional[str] = Field(...)
    created_at: str
    updated_at: str
    due_at: Optional[str]
    lock_at: Optional[str]
    unlock_at: Optional[str]
    has_overrides: Optional[bool]
    all_dates: Optional[list]
    course_id: int
    html_url: Optional[str]
    submission_download_url: Optional[str]
    assignment_group_id: int
    due_date_required: bool
    allowed_extensions: Optional[list]
    max_name_length: int
    turnitin_enabled: Optional[bool]
    vericite_enabled: Optional[bool]
    turnitin_settings: Optional[dict]
    grade_group_students_individually: bool
    external_tool_tag_attributes: Optional[dict]
    peer_reviews: bool
    automatic_peer_reviews: bool
    peer_review_count: Optional[int]
    peer_reviews_assign_at: Optional[str]
    intra_group_peer_reviews: bool
    group_category_id: Optional[int] = Field(...)
    needs_grading_count: Optional[int]
    needs_grading_count_by_section: Optional[list]
    position: int
    post_to_sis: Optional[bool]
    integration_id: Optional[str]
    integration_data: Optional[dict]
    points_possible: Optional[float]
    submission_types: list
    has_submitted_submissions: bool
    grading_type: str
    grading_standard_id: Optional[bool] = Field(...)
    published: bool
    unpublishable: Optional[bool]
    only_visible_to_overrides: bool
    locked_for_user: bool
    locked_info: Optional[str]
    lock_explanation: Optional[str]
    quiz_id: Optional[int]
    anonymous_submissions: Optional[bool]
    discussion_topic: Optional[dict]
    freeze_on_copy: Optional[bool]
    frozen: Optional[bool]
    frozen_attributes: Optional[list]
    submission: Optional[dict]
    use_rubric_for_grading: Optional[bool]
    rubric_settings: Optional[dict]
    rubric: Optional[list]
    assignment_visibility: Optional[list]
    overrides: Optional[list]
    omit_from_final_grade: Optional[bool]
    moderated_grading: bool
    grader_count: int
    final_grader_id: Optional[int] = Field(...)
    grader_comments_visible_to_graders: Optional[bool]
    graders_anonymous_to_graders: Optional[bool]
    grader_names_visible_to_final_grader: Optional[bool]
    anonymous_grading: bool
    post_manually: bool
    score_statistics: Optional[list]
    can_submit: Optional[bool]
    annotatable_attachment_id: Optional[bool] = Field(...)
    anonymize_students: Optional[bool]
    require_lockdown_browser: Optional[bool]
    important_dates: Optional[bool]
    muted: Optional[bool]
