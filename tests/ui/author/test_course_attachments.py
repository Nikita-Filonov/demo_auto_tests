import allure
import pytest
from assertions import assert_attr

from settings import RERUNS, RERUNS_DELAY
from utils.allure.stories.ui.author import AuthorStory
from utils.api.utils import COMMON_FILES
from utils.utils import file_name_or_path_resolve


@pytest.mark.ui
@pytest.mark.author_course_attachments
@allure.epic('Core LMS')
@allure.feature('Author (UI)')
@allure.story(AuthorStory.COURSE_ATTACHMENTS.value)
@pytest.mark.flaky(reruns=RERUNS, reruns_delay=RERUNS_DELAY)
@allure.severity(allure.severity_level.CRITICAL)
class TestCourseAttachmentsUi:
    file = file_name_or_path_resolve(COMMON_FILES[0])
    file_path = COMMON_FILES[0]

    @allure.id("4227")
    @allure.title('Author uploads file to the course (UI)')
    @pytest.mark.parametrize('file_path', COMMON_FILES)
    def test_author_uploads_file_to_the_course(self, course_files, file_path):
        course_files.upload_file(file_path)
        course_files.text_present(file_name_or_path_resolve(file_path))

    @allure.id("4230")
    @allure.title('Author checks possibility to replace file with existing name (UI)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_author_checks_possibility_to_replace_file_with_existing_name(self, course_files, author):
        course_files.upload_file(self.file_path)
        course_files.click_confirm_modal_yes_button()
        files_count = course_files.file_row.count(file_name=self.file)
        assert_attr(files_count, 1, f'Number of files "{self.file}"')

    @allure.id("4228")
    @allure.title('Author removes file from the course (UI)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_author_removes_file_from_the_course(self, course_files, author):
        course_files.click_remove_file(self.file)
        course_files.click_confirm_modal_yes_button()
        course_files.text_not_present(self.file)

    @allure.id("4226")
    @allure.title('Author copies file link from the course (UI)')
    @pytest.mark.parametrize('author', [{'files': COMMON_FILES}], indirect=['author'])
    def test_author_copies_file_link_from_the_course(self, course_files, author):
        course_files.click_copy_file(self.file)
        course_files.file_link_copied(self.file)
