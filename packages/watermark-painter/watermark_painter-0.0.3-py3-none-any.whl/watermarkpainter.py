import datetime
import sys
from logging import Logger

from win32com.client import Dispatch


class WatermarkPainter(object):
    """
    add watermark to doc file
    """

    __GwdStatisticPages = 2
    __GmsoShapeRectangle = 1

    def __init__(self, image_filepath):
        self.__img_filepath = image_filepath

    def draw_on_doc(self, doc_filepath):
        """
        add watermark to doc file and save
        :param doc_filepath:
        :return:
        """
        return self.draw_to_doc(doc_filepath, "")

    def draw_to_doc(self, src_doc_filepath, des_doc_filepath):
        """
        add watermark to doc file, then save as another file
        :param src_doc_filepath:
        :param des_doc_filepath:
        :return:
        """

        # des_doc_filepath is valid
        if des_doc_filepath and des_doc_filepath.strip() != "":
            pass
        else:
            dt = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            if ".docx" in src_doc_filepath:
                des_doc_filepath = src_doc_filepath.replace(".docx", "_" + dt + ".docx")
            elif ".doc" in src_doc_filepath:
                des_doc_filepath = src_doc_filepath.replace(".doc", "_" + dt + ".doc")
            else:
                raise Exception("Bad Argument")

        app = Dispatch('Word.Application')
        app.visible = True

        doc = app.Documents.Open(src_doc_filepath)

        try:
            ps = doc.PageSetup
            page_height = ps.PageHeight
            page_width = ps.PageWidth
            top_offset = (page_height - page_width) / 2

            # get page count
            app.ActiveDocument.Repaginate()
            page_count = app.ActiveDocument.ComputeStatistics(self.__GwdStatisticPages)

            # focus at top
            for k in range(1, page_count + 1):
                app.Application.Browser.Previous()

            for k in range(1, page_count + 1):

                if k > 1:
                    app.ActiveDocument.Shapes.AddShape(self.__GmsoShapeRectangle, 0, top_offset,
                                                       page_width, page_width).Select()

                    app.Selection.ShapeRange.Fill.Transparency = 0.85
                    app.Selection.ShapeRange.Fill.UserPicture(self.__img_filepath)

                    app.Selection.ShapeRange.Line.Weight = 0.75
                    app.Selection.ShapeRange.Line.Transparency = 0  #
                    app.Selection.ShapeRange.Line.Visible = 0

                    app.Selection.ShapeRange.LockAnchor = False
                    app.Selection.ShapeRange.LockAspectRatio = 0

                    app.Selection.ShapeRange.WrapFormat.AllowOverlap = True
                    app.Selection.ShapeRange.WrapFormat.Type = 3

                doc.Application.Browser.Next()

            doc.SaveAs(des_doc_filepath)
        except Exception as ex:
            Logger.exception(sys.exc_info())
        finally:
            doc.Close()

        return des_doc_filepath
