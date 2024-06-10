from collections import defaultdict
from typing import Optional
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import pyqtSlot

from pss_cli.core.logging import logger
from pss_cli.gui.dialogs.simple_dialog import SimpleDialog
from pss_cli.core.controllers import ControllerFactory
from pss_cli.core.database import db
from pss_cli.gui.widgets.searchable_combobox import SearchableQComboBox


class AddGeneratingSystem(SimpleDialog):
    """Add a generating system to the database"""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        controller_factory = ControllerFactory()
        self.controller = controller_factory.create_controller("generating_system")
        self.generator_controller = controller_factory.create_controller("generator")
        super().__init__(parent)

    def init_ui(self):
        self.setWindowTitle("Add Generating system to the database")

        cases = db.select_table("case")

        if not cases:
            logger.error("No cases found in the database")

        self.case_name_edit = QtWidgets.QComboBox()
        self.case_name_edit.addItems([str(case.name) for case in cases])  # type: ignore
        self.case_description = QtWidgets.QLabel()
        self.case_filepath = QtWidgets.QLabel()

        self.gs_name_edit = QtWidgets.QLineEdit()
        self.from_bus_no = SearchableQComboBox()
        self.from_bus_name = QtWidgets.QLabel()
        self.to_bus_no = SearchableQComboBox()
        self.to_bus_name = QtWidgets.QLabel()
        self.branch_id = SearchableQComboBox()
        self.reversed = QtWidgets.QCheckBox()

        self.generators = []
        self.machine_ids = []
        self.add_generator_button = QtWidgets.QPushButton("Add Generator")

        self.add_widget(self.case_name_edit, "Case Name", required=True)
        self.add_widget(self.case_description, "Case Description", required=False)
        self.add_widget(self.case_filepath, "Case Filepath", required=False)
        self.add_widget(self.gs_name_edit, "Name", required=True)
        self.add_widget(self.from_bus_no, "From Bus No", required=True)
        self.add_widget(self.from_bus_name, "From Bus Name", required=False)
        self.add_widget(self.to_bus_no, "To Bus No", required=True)
        self.add_widget(self.to_bus_name, "To Bus Name", required=False)
        self.add_widget(self.branch_id, "Branch Id", required=True)
        self.add_widget(self.reversed, "Reversed", required=False)
        self.add_widget(self.add_generator_button, required=False)

        if cases:
            self.update_case_info()
            self.update_from_bus_name()
            self.update_to_bus_name()
            self.update_generators()

        self.case_name_edit.currentTextChanged.connect(self.update_case_info)
        self.from_bus_no.currentTextChanged.connect(self.update_from_bus_name)
        self.to_bus_no.currentTextChanged.connect(self.update_to_bus_name)
        self.from_bus_no.currentIndexChanged.connect(self.update_to_bus_numbers)
        self.add_generator_button.clicked.connect(self.add_generator)

    @pyqtSlot()
    def add_generator(self) -> None:
        """Add a generator combobox to the dialog."""

        self.add_generator_button.setStyleSheet("")
        generator = SearchableQComboBox()
        machine_id = SearchableQComboBox()
        self.generators.append(generator)
        self.machine_ids.append(machine_id)
        self.clear_required_label()
        self.clear_accept_cancel_buttons()
        self.add_widget(generator, f"Generator {len(self.generators)}", required=True)
        self.add_widget(machine_id, f"Machine Id {len(self.generators)}", required=True)
        self.add_required_label()
        self.add_buttons()
        self.update_generators(last_only=True)
        self.update_machine_ids(last_only=True)

        generator.currentTextChanged.connect(self.update_machine_ids)

    def update_machine_ids(
        self, bus_no: Optional[float] = None, last_only: bool = False
    ) -> None:
        """Update the machine ids based on the selected case and generator bus numbers."""

        case = self.controller.get_case(self.case_name_edit.currentText())

        if last_only:
            try:
                generator_bus_number = int(self.generators[-1].currentText())
                self.generators[-1].setStyleSheet("")
            except ValueError:
                self.generators[-1].setStyleSheet("border: 1px solid red")
                return
            machine_ids = self.controller.get_machine_ids(generator_bus_number, case)
            if not machine_ids:
                self.machine_ids[-1].clear()
                return
            self.machine_ids[-1].clear()
            self.machine_ids[-1].addItems(machine_ids)
            self.machine_ids[-1].set_searchable()
            return

        for generator, machine_id in zip(self.generators, self.machine_ids):
            try:
                generator_bus_number = int(generator.currentText())
                generator.setStyleSheet("")
            except ValueError:
                generator.setStyleSheet("border: 1px solid red")
                return
            machine_ids = self.controller.get_machine_ids(generator_bus_number, case)
            if not machine_ids:
                machine_id.clear()
                continue
            machine_id.clear()
            machine_id.addItems(machine_ids)
            machine_id.set_searchable()

    def update_generators(self, last_only: bool = False) -> None:
        """Update the generators based on the selected case and bus numbers."""

        case = self.controller.get_case(self.case_name_edit.currentText())
        if not case:
            return
        generator_bus_numbers = [
            str(bus_number)
            for bus_number in self.controller.get_generator_bus_numbers(case)
        ]
        if not generator_bus_numbers:
            self.generators[-1].clear()
            return
        if last_only:
            self.generators[-1].clear()
            self.generators[-1].addItems(generator_bus_numbers)
            self.generators[-1].set_searchable()
            return

        for generator in self.generators:
            generator.clear()
            generator.addItems(generator_bus_numbers)
            generator.set_searchable()

    def update_branch_ids(self) -> None:
        """Update the branch ids based on the selected case and bus numbers."""

        case = self.controller.get_case(self.case_name_edit.currentText())
        from_bus_no = int(self.from_bus_no.currentText())
        to_bus_no = int(self.to_bus_no.currentText())
        branch_ids = self.controller.get_branch_ids(case, from_bus_no, to_bus_no)
        if not branch_ids:
            self.branch_id.clear()
            return
        str_branch_ids = [str(branch_id) for branch_id in branch_ids]
        self.branch_id.clear()
        self.branch_id.addItems(str_branch_ids)
        self.branch_id.set_searchable()

    def update_to_bus_numbers(self) -> None:
        """Update the to bus numbers based on the selected case and from bus number."""

        case = self.controller.get_case(self.case_name_edit.currentText())
        try:
            from_bus_no = int(self.from_bus_no.currentText())
        except ValueError:
            return
        bus_numbers = self.controller.get_branch_to_bus_numbers(case, from_bus_no)
        str_bus_numbers = [str(bus_no) for bus_no in bus_numbers]
        self.to_bus_no.clear()
        self.to_bus_no.addItems(str_bus_numbers)
        self.to_bus_no.set_searchable()
        self.update_branch_ids()

    def update_from_bus_name(self) -> None:
        """Update the bus name based on the selected case and bus number."""

        case = self.controller.get_case(self.case_name_edit.currentText())
        try:
            from_bus_number = int(self.from_bus_no.currentText())
            self.from_bus_no.setStyleSheet("")
        except ValueError:
            self.from_bus_no.setStyleSheet("border: 1px solid red")
            return
        if from_bus_number == "":
            self.from_bus_name.setText("")
            return

        from_bus_name = self.controller.get_bus_name(case, from_bus_number)
        if not from_bus_name:
            self.from_bus_name.setText("")
            return
        self.from_bus_name.setText(from_bus_name)

    def update_to_bus_name(self) -> None:
        """Update the bus name based on the selected case and bus number"""

        case = self.controller.get_case(self.case_name_edit.currentText())
        try:
            to_bus_number = int(self.to_bus_no.currentText())
            self.to_bus_no.setStyleSheet("")
        except ValueError:
            self.to_bus_no.setStyleSheet("border: 1px solid red")
            return
        if to_bus_number == "":
            self.to_bus_name.setText("")
            return
        to_bus_name = self.controller.get_bus_name(case, to_bus_number)
        if not to_bus_name:
            self.to_bus_name.setText("")
            return
        self.to_bus_name.setText(to_bus_name)

    def check_duplicated_generators(self) -> bool:
        """Check if there are duplicated generators in the dialog."""

        generator_bus_numbers = [
            generator.currentText() for generator in self.generators
        ]
        machine_ids = [machine_id.currentText() for machine_id in self.machine_ids]

        counter = defaultdict(int)
        for generator_bus_number, machine_id in zip(generator_bus_numbers, machine_ids):
            counter[(generator_bus_number, machine_id)] += 1

        if any(value > 1 for value in counter.values()):
            return True

        return False

    @pyqtSlot()
    def update_case_info(self) -> None:
        """Update the case description, file path and bus numbers based on the selected case."""

        case = self.controller.get_case(self.case_name_edit.currentText())
        self.case_description.setText(case.description)
        self.case_filepath.setText(case.file_path)

        bus_numbers = self.controller.get_branch_from_bus_numbers(case)
        str_bus_numbers = [str(bus_no) for bus_no in sorted(list(set(bus_numbers)))]
        self.from_bus_no.clear()
        self.from_bus_no.addItems(str_bus_numbers)
        self.from_bus_no.set_searchable()
        self.update_to_bus_numbers()
        self.update_generators()
        self.update_machine_ids()

    @pyqtSlot()
    def accept(self):
        if self.check_duplicated_generators():
            for generator, machine_id in zip(self.generators, self.machine_ids):
                generator.setStyleSheet("border: 1px solid red")
                machine_id.setStyleSheet("border: 1px solid red")
            logger.error("Duplicated generators found")
            return

        if not self.generators or not self.machine_ids:
            self.add_generator_button.setStyleSheet("border: 1px solid red")
            logger.error("Please add a generator to the generating system")
            return

        case = self.controller.get_case(self.case_name_edit.currentText())
        self.controller.add(
            name=self.gs_name_edit.text(),
            case=case,
            from_bus_no=int(self.from_bus_no.currentText()),
            to_bus_no=int(self.to_bus_no.currentText()),
            branch_id=self.branch_id.currentText(),
            reversed=self.reversed.isChecked(),
        )

        gs = self.controller.get_generating_system(self.gs_name_edit.text(), case)
        if not gs:
            logger.error("Generating system not found")
            return

        for generator, machine_id in zip(self.generators, self.machine_ids):
            self.generator_controller.add(
                bus_number=generator.currentText(),
                machine_id=machine_id.currentText(),
                generating_system=gs,
            )

        self.close()

    @pyqtSlot()
    def cancel(self):
        self.close()
