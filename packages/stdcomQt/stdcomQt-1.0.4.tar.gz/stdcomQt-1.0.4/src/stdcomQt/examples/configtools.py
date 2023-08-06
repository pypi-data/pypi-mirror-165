from PyQt5.QtWidgets import QApplication
from stdcomutilitywidgets import StecIPconfigDialog, StecPostgresConfigWidget
import  sys, os

if __name__=="__main__":

    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.
    sys.path.append(parent)


    def callBack(ip, port):
        print("Address: ", ip, " Service Port: ", port)
    def cancel() :
        print("Cancel")

    def postCallback( a,b,c,d,e ) :
        print(a,b,c,d,e)

    app = QApplication(sys.argv)
    w = StecIPconfigDialog(callBack, cancel)
    w.show()
    p = StecPostgresConfigWidget(postCallback, cancel)
    p.show()
    sys.exit(app.exec_())