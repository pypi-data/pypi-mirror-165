
# Library Imports
# import pandas as pd
# from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Local Imports
# from hoodat_utils import gs
from hoodat_utils import models as m


class create_dataset():

    def __init__(self, series_name, sqlalchemy_database_uri):
        self.series_name = series_name
        self.sqlalchemy_database_uri = sqlalchemy_database_uri
        self.engine = create_engine(self.sqlalchemy_database_uri)

    def query_series_character_labels(self):
        query = self.session.query(
            m.Series.series_id, m.Video.video_id, m.Video.video_type, m.Video.save_name, m.Frame.frame_id,
            m.Frame.frame_number, m.Object.object_id,
            m.Character_Label.character_label_id, m.Object.object_x,
            m.Object.object_y, m.Object.object_w, m.Object.object_h,
            m.Object.object_cascade, m.Character.character_name
        ).filter(
            m.Series.series_name == self.series_name
        ).join(m.Episode).join(m.Video).join(m.Frame).join(m.Object).join(m.Character_Label).join(m.Character)
        series_character_labels = query.all()
        print("Number of labels: {0}".format(str(len(series_character_labels))))
        return series_character_labels
