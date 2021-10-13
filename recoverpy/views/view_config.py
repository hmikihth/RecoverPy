from py_cui import PyCUI

from recoverpy.config import config as CONFIG
from recoverpy.utils.logger import LOGGER
from recoverpy.utils.saver import SAVER


class ConfigView:
    def __init__(self, master: PyCUI):
        self.master = master
        self._log_enabled = LOGGER.log_enabled
        self.create_ui_content()

    def create_ui_content(self):
        """Handle the creation of the UI elements."""
        self.save_path_box = self.master.add_text_box(
            title="Save Path",
            row=0,
            column=1,
            row_span=1,
            column_span=8,
            padx=0,
            pady=0,
            initial_text=SAVER.save_path,
        )
        self.master.add_button(
            "Save",
            row=1,
            column=8,
            row_span=1,
            column_span=1,
            padx=0,
            pady=0,
            command=self.set_save_path,
        ).set_color(1)
        self.log_path_box = self.master.add_text_box(
            title="Log Path",
            row=2,
            column=1,
            row_span=1,
            column_span=8,
            padx=0,
            pady=0,
            initial_text=LOGGER.log_path,
        )
        self.master.add_button(
            "Save",
            row=3,
            column=8,
            row_span=1,
            column_span=1,
            padx=0,
            pady=0,
            command=self.set_log_path,
        ).set_color(1)
        self.master.add_label(
            title="Enable Logging",
            row=4,
            column=4,
            row_span=1,
            column_span=2,
            padx=0,
            pady=0,
        )
        self.yes_button = self.master.add_button(
            "Yes",
            row=5,
            column=3,
            row_span=1,
            column_span=1,
            padx=0,
            pady=0,
            command=self.enable_logging,
        )
        self.no_button = self.master.add_button(
            "No",
            row=5,
            column=6,
            row_span=1,
            column_span=1,
            padx=0,
            pady=0,
            command=self.disable_logging,
        )
        self.master.add_button(
            "Save & Exit",
            row=8,
            column=2,
            row_span=1,
            column_span=2,
            padx=0,
            pady=0,
            command=None,
        ).set_color(4)
        self.master.add_button(
            "Cancel",
            row=8,
            column=6,
            row_span=1,
            column_span=2,
            padx=0,
            pady=0,
            command=None,
        ).set_color(2)

        self.set_yes_no_colors()

    def set_save_path(self):
        user_input = self.save_path_box.get()
        if not CONFIG.path_is_valid(path=user_input):
            self.master.show_error_popup("Path invalid", "Given save path is invalid.")
            return

        CONFIG.write_config(
            save_path=user_input,
            log_path=LOGGER.log_path,
            enable_logging=LOGGER.log_enabled,
        )

        self.master.show_message_popup("", "Save path changed successfully")

    def set_log_path(self):
        user_input = self.log_path_box.get()
        if not CONFIG.path_is_valid(path=user_input):
            self.master.show_error_popup("Path invalid", "Given log path is invalid.")
            return

        CONFIG.write_config(
            save_path=SAVER.save_path,
            log_path=user_input,
            enable_logging=LOGGER.log_enabled,
        )

        self.master.show_message_popup("", "Log path changed successfully")

    def set_log_state(self):
        CONFIG.write_config(
            save_path=SAVER.save_path,
            log_path=LOGGER.log_path,
            enable_logging=self._log_enabled,
        )

    def enable_logging(self):
        if self._log_enabled:
            return

        self._log_enabled = True
        self.set_log_state()
        self.set_yes_no_colors()

        self.master.show_message_popup("", "Logging enabled")

    def disable_logging(self):
        if not self._log_enabled:
            return

        self._log_enabled = False
        self.set_log_state()
        self.set_yes_no_colors()

        self.master.show_message_popup("", "Logging disabled")

    def set_yes_no_colors(self):
        if self._log_enabled:
            self.yes_button.set_color(4)
            self.no_button.set_color(1)
        else:
            self.yes_button.set_color(1)
            self.no_button.set_color(4)

    def save_all(self):
        save_path = self.save_path_box.get()
        log_path = self.log_path_box.get()
        if not CONFIG.path_is_valid(path=save_path):
            self.master.show_error_popup("Path invalid", "Given save path is invalid.")
            return
        if not CONFIG.path_is_valid(path=log_path):
            self.master.show_error_popup("Path invalid", "Given Log path is invalid.")
            return

        CONFIG.write_config(
            save_path=save_path,
            log_path=log_path,
            enable_logging=self._log_enabled,
        )
