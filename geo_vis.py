from geoplotlib.layers import BaseLayer
from geoplotlib.core import BatchPainter
import geoplotlib
from geoplotlib.colors import colorbrewer
from geoplotlib.utils import epoch_to_str, BoundingBox, read_csv


class AllTrailsLayer(BaseLayer):
    def __init__(self, map_data):
        self.data = map_data
        self.color_map = colorbrewer(self.data['runner_id'], alpha=220)
        self.t = self.data['timestamp'].min()
        self.painter = BatchPainter()

    def draw(self, proj, mouse_x, mouse_y, ui_manager):
        self.painter = BatchPainter()
        df = self.data.where((self.data['timestamp'] > self.t) & (self.data['timestamp'] <= self.t + 15 * 60))

        for taxi_id in set(df['runner_id']):
            grp = df.where(df['runner_id'] == taxi_id)
            self.painter.set_color(self.color_map[taxi_id])
            x, y = proj.lonlat_to_screen(grp['lon'], grp['lat'])
            self.painter.points(x, y, 10)

        self.t += 60

        if self.t > self.data['timestamp'].max():
            self.t = self.data['timestamp'].min()

        self.painter.batch_draw()
        ui_manager.info(epoch_to_str(self.t))

    # this should get modified as well moving forward. Might be too small, should be dynamic based on data
    def bbox(self):
        return BoundingBox(north=37.801421, west=-122.517339, south=37.730097, east=-122.424474)

# if __name__ == '__main__':
#     data = read_csv('users/0_alex/alex.csv')
#     geoplotlib.add_layer(AllTrailsLayer(map_data=data))
#     geoplotlib.show()
