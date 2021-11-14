import pcbnew
import FootprintWizardBase
import PadArray as PA

class ModuleWizard(FootprintWizardBase.FootprintWizard):

    def GetName(self):
        return "Module"

    def GetDescription(self):
        return "Module footprint wizard"


    def GenerateParameterList(self):
        self.AddParam("Pads", "n_vertical", self.uInteger, 12, min_value=1)
        self.AddParam("Pads", "n_horizontal", self.uInteger, 10, min_value=1)
        self.AddParam("Pads", "width", self.uMM, 0.7112, min_value=0.25)
        self.AddParam("Pads", "length", self.uMM, 2.032, min_value=0.25)
        self.AddParam("Pads", "h_pitch", self.uMM, 1.27, min_value=0.25)
        self.AddParam("Pads", "v_pitch", self.uMM, 1.27, min_value=0.25)

        self.AddParam("Package", "width", self.uMM, 17.5, min_value=5)
        self.AddParam("Package", "length", self.uMM, 28.7, min_value=5)
        self.AddParam("Package", "v_space", self.uMM, 3.04, min_value=0.25)
        self.AddParam("Package", "h_space", self.uMM, 3.04, min_value=0.25)

    @property
    def pads(self):
        return self.parameters['Pads']

    @property
    def package(self):
        return self.parameters['Package']

    def GetValue(self):
        n = self.pads['n_vertical'] * 2 + self.pads['n_horizontal']
        width = pcbnew.ToMM(self.package['width'])
        length = pcbnew.ToMM(self.package['length'])
        return f"Module-{n}_{width}x{length}mm"

    def CheckParameters(self):
        pass

    def BuildThisFootprint(self):
        width = self.package['width']
        length = self.package['length']
        v_space = self.package['v_space']
        h_space = self.package['h_space']

        pad_n_vertical = self.pads["n_vertical"]
        pad_n_horizontal = self.pads["n_horizontal"]
        pad_width = self.pads["width"]
        pad_length = self.pads["length"]
        pad_h_pitch = self.pads["h_pitch"]
        pad_v_pitch = self.pads["v_pitch"]


        h_pad = PA.PadMaker(self.module).SMDPad( pad_length, pad_width, 
            shape=pcbnew.PAD_SHAPE_ROUNDRECT, rot_degree=90.0)
        v_pad = PA.PadMaker(self.module).SMDPad( pad_length, pad_width,
            shape=pcbnew.PAD_SHAPE_ROUNDRECT)


        yCenterVerticalRow = (pad_n_vertical - 1) * pad_v_pitch / 2
        #left row
        centerLeftRow = pcbnew.wxPoint(-width /2, yCenterVerticalRow)
        array = PA.PadLineArray(h_pad, pad_n_vertical, pad_v_pitch, True, centerLeftRow)
        array.SetFirstPadInArray(1)
        array.AddPadsToModule(self.draw)

        #right row
        centerRightRow = pcbnew.wxPoint(width /2, yCenterVerticalRow)
        array = PA.PadLineArray(h_pad, pad_n_vertical, -pad_v_pitch, True, centerRightRow)
        array.SetFirstPadInArray(pad_n_vertical + pad_n_horizontal + 1)
        array.AddPadsToModule(self.draw)

        #bottom row
        yBottomRow = (pad_n_vertical - 1) * pad_v_pitch + v_space
        centerBottomRow = pcbnew.wxPoint(0, (pad_n_vertical - 1) * pad_v_pitch + v_space)
        array = PA.PadLineArray(v_pad, pad_n_horizontal, pad_h_pitch, False, centerBottomRow)
        array.SetFirstPadInArray(pad_n_vertical + 1)
        array.AddPadsToModule(self.draw)

        # Silkscreen
        self.draw.SetLayer(pcbnew.F_SilkS)
        offset = self.draw.GetLineThickness() / 2
        self.draw.Polyline([
            [ -width/2 - offset, yBottomRow + offset],
            [ -width/2 - offset, yBottomRow - length - offset],
            [ width/2 + offset, yBottomRow - length - offset],
            [ width/2 + offset, yBottomRow + offset],
            [ -width/2 - offset, yBottomRow + offset],
        ])

        # Courtyard
        offset = pad_length / 2
        self.draw.SetLayer(pcbnew.F_CrtYd)
        self.draw.Polyline([
            [ -width/2 - offset, yBottomRow + offset],
            [ -width/2 - offset, yBottomRow - length - offset],
            [ width/2 + offset, yBottomRow - length - offset],
            [ width/2 + offset, yBottomRow + offset],
            [ -width/2 - offset, yBottomRow + offset],
        ])

ModuleWizard().register()