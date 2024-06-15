import pandas as pd
from lib.converte import UnitConverter

class Annulus:
    def __init__(self, x_center, y_center, inner_radius, outer_radius):
        self.x_center = x_center
        self.y_center = y_center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius

    def calculate_radius(self):
        # Convertendo de pixel para arcsec e calculando o raio
        inner_radius_arcsec = self.inner_radius * 0.492
        outer_radius_arcsec = self.outer_radius * 0.492
        return inner_radius_arcsec + (outer_radius_arcsec - inner_radius_arcsec) / 2


class Pie:
    
    def __init__(self, x_center, y_center, inner_radius, outer_radius, angle_start, angle_end):
        self.x_center = x_center
        self.y_center = y_center
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.angle_start = angle_start
        self.angle_end = angle_end

    def calculate_radius(self):
        # Convertendo de pixel para arcsec e calculando o raio
        inner_radius_arcsec = self.inner_radius * 0.492
        outer_radius_arcsec = self.outer_radius * 0.492
        return inner_radius_arcsec + (outer_radius_arcsec - inner_radius_arcsec) / 2


class RegionProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.regions = []
        self.list_innerradius = []
        self.list_outradius = []
        self.list_erro_region = []

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith('annulus'):
                region_data = self._parse_annulus(line)
                self.regions.append(Annulus(*region_data))
                
            elif line.startswith('pie'):
                region_data = self._parse_pie(line)
                self.regions.append(Pie(*region_data))

    def _parse_annulus(self, line):
        parts = line[line.find('(') + 1 : line.find(')')].split(',')
        x_center = float(parts[0])
        y_center = float(parts[1])
        inner_radius = float(parts[2])
        outer_radius = float(parts[3])
        return x_center, y_center, inner_radius, outer_radius

    def _parse_pie(self, line):
        parts = line[line.find('(') + 1 : line.find(')')].split(',')
        x_center = float(parts[0])
        y_center = float(parts[1])
        inner_radius = float(parts[2])
        outer_radius = float(parts[3])
        angle_start = float(parts[4])
        angle_end = float(parts[5])
        return x_center, y_center, inner_radius, outer_radius, angle_start, angle_end
    
    def make_inner_radius_list(self):
        self.parse_file()
        for i in self.regions:
            self.list_innerradius.append(i.inner_radius)
        
    def make_out_radius_list(self):
        self.parse_file()
        for i in self.regions:
            self.list_outradius.append(i.outer_radius)  

    def erro_region(self):
        self.make_inner_radius_list()
        self.make_out_radius_list()
        print(len(self.list_innerradius))
        print(len(self.list_outradius))
        for i in range(len(self.list_innerradius)):
            self.list_erro_region.append(self.list_outradius[i]-self.list_innerradius[i])


    def arcsec_Radius(self,redshift):
        self.parse_file()
        radii = [region.calculate_radius() for region in self.regions if isinstance(region, (Annulus, Pie))]
        
        return radii
   
    def kpc_Radius(self,redshift):
        self.parse_file()
        radii = [UnitConverter.arcsec_to_kpc(region.calculate_radius(),redshift) for region in self.regions if isinstance(region, (Annulus, Pie))]
        return radii
    
    def Mpc_Radius(self,redshift):
        self.parse_file()
        radii = [UnitConverter.arcsec_to_mpc(region.calculate_radius(),redshift) for region in self.regions if isinstance(region, (Annulus, Pie))]
        return radii
    
    def pixel_Radius(self,redshift):
        self.parse_file()
        radii = [UnitConverter.arcsec_to_pixel(region.calculate_radius(),redshift) for region in self.regions if isinstance(region, (Annulus, Pie))]
        return radii



