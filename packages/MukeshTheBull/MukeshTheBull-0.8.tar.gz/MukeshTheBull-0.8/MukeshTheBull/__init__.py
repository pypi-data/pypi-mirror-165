class Moo:
  def __init__(self):
    print("Moooo! Welcome to my GauShala aka Cowshed!! Mooo ")
    print("Instructions\n Moo.SeeMe() \n Moo.SeeMom()\nMoo.SeeDad()\nMoo.SeeFriends()")
    from PIL import Image
    import urllib.request 
    

  def SeeMe(self):
    print("Why not! Have a look ")
    from PIL import Image
    import urllib.request 
    url = "https://i.ibb.co/hgNYffS/mukesh.png"
    im = Image.open(urllib.request.urlopen(url))
    im.show()
    

  def SeeMom(self):
    print("Why not! Have a look ")
    from PIL import Image
    import urllib.request 
    url = "https://i.ibb.co/7JrJf9w/mom.png"
    im = Image.open(urllib.request.urlopen(url))
    im.show()

  def SeeDad(self):
    print("Why not! Have a look ")
    from PIL import Image
    import urllib.request 
    url = "https://i.ibb.co/x5FwTQt/dad.png"
    im = Image.open(urllib.request.urlopen(url))
    im.show()

  def SeeFriends(self):
    print("Why not! Have a look ")
    from PIL import Image
    import urllib.request 
    url = "https://i.ibb.co/5LCjZJx/friends.png"
    im = Image.open(urllib.request.urlopen(url))
    im.show()
