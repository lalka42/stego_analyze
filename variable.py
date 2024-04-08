
class Variable:
    def __init__(self, **kwargs):
        self.path_analyze_dump = kwargs.get('path')
        self.path_dataset_dump = kwargs.get('path')
        self.path_new_model = kwargs.get('path')
        self.path_analyze_res = kwargs.get('path')
        self.path_dataset_res = kwargs.get('path')

        # self.save_diag = False
        self.mean_diag = False
        self.prepare_set_path = kwargs.get('path')
        self.mode = 0
        self.stop_rts = False
        self.selected_iface = None
        self.selected_dataset_res_type = "Excel"
        self.rts_df = None


    def change_dataset_res_type(self, type):
        self.selected_dataset_res_type = type
    def change_analyze_dump_path(self, path):
        self.path_analyze_dump = path

    def change_dataset_dump_path(self, path):
        self.path_dataset_dump = path

    def change_dataset_res_path(self, path):
        self.path_dataset_res = path

    def change_new_model_path(self, path):
        self.path_new_model = path

    def change_program_mode(self, mode):
        self.mode = mode

    def rts_analyze_stop(self):
        self.stop_rts = True

    def rts_analyze_restore(self):
        self.stop_rts = False

    def change_analyze_res_path(self, path):
        self.path_analyze_res = path

    # def change_save_diag(self, diag):
    #     self.save_diag = diag

    def change_mean_diag(self, diag):
        self.mean_diag = diag

    def change_iface(self, iface):
        self.selected_iface = iface

    def change_rts_row(self, row):
        self.rts_row = row


variable = Variable()
