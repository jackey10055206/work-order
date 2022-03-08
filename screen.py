    self.app = QApplication.instance()
        screen_resolution = self.app.desktop().screenGeometry() #1920X1080
        print(screen_resolution)
        self.hw_ratio = 1080/1920
        self.ratio_width = screen_resolution.width()/1920
        if self.ratio_width < 1:
            self.ratio_width = 1
        self.ratio_height = screen_resolution.height()/1080
        if self.ratio_height < 1:
            self.ratio_height = 1
        self.ratio_width = int(self.ratio_width)
        self.ratio_height = int(self.ratio_height)
        self._init_ui_size()

    def _init_ui_size(self):
        self._resize_with_ratio(self)
        for q_widget in self.findChildren(QWidget):
            #print(q_widget.objectName())
            self._resize_with_ratio(q_widget)
            self._move_with_ratio(q_widget)
            for q_widget in self.findChildren(QAbstractScrollArea):
                self._resize_with_ratio(q_widget)
                self._move_with_ratio(q_widget)

    def _resize_with_ratio(self, input_ui):
        input_ui.resize(input_ui.width() * self.ratio_width, input_ui.height() * self.ratio_height)
    def _move_with_ratio(self, input_ui):
        input_ui.move(input_ui.x() * self.ratio_width, input_ui.y() * self.ratio_height)