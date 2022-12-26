from extensions.graph import Node, Edge, Color, TrackType
from extensions.cards import Ticket


class InvalidGame(Exception):
    "Raised when map name is not recognised."
    pass


class Map():
    def __init__(self, map: str):
        """ Class for representing a map. """
        self.nodes = []
        self.edges = []
        self.tickets = []

        if map.lower() == "europe":
            self.init_europe()
        else:
            raise InvalidGame(f"Map not recognised: {map}")
    
    def __repr__(self):
        return self.name


    def init_europe(self):
        """ Initiates the map of Ticket to Ride: Europe. """
        self.name = "Europe"
        self.filename = "europe.jpg"
        self.color_filename = "europe_color.jpg"
        self.height = 800
        self.width = 1321

        # Nodes
        lisbon = Node("Lisbon", add_to = self.nodes, x=31, y=713)
        cadiz = Node("Cádiz", add_to = self.nodes, x=110, y=777)
        madrid = Node("Madrid", add_to = self.nodes, x=112, y=685)
        pamplona = Node("Pamplona", add_to = self.nodes, x=233, y=586)
        barcelona = Node("Barcelona", add_to = self.nodes, x=248, y=698)
        paris = Node("Paris", add_to = self.nodes, x=312, y=399)
        dieppe = Node("Dieppe", add_to = self.nodes, x=251, y=344)
        brest = Node("Brest", add_to = self.nodes, x=141, y=380)
        london = Node("London", add_to = self.nodes, x=264, y=234)
        edinburgh = Node("Edinburgh", add_to = self.nodes, x=183, y=51)
        amsterdam = Node("Amsterdam", add_to = self.nodes, x=382, y=239)
        bruxelles = Node("Bruxelles", add_to = self.nodes, x=355, y=296)
        essen = Node("Essen", add_to = self.nodes, x=481, y=249)
        zurich = Node("Zürich", add_to = self.nodes, x=452, y=466)
        marseille = Node("Marseille", add_to = self.nodes, x=418, y=581)
        frankfurt = Node("Frankfurt", add_to = self.nodes, x=463, y=336)
        munchen = Node("München", add_to = self.nodes, x=534, y=389)
        venezia = Node("Venezia", add_to = self.nodes, x=554, y=506)
        roma = Node("Roma", add_to = self.nodes, x=563, y=616)
        palermo = Node("Palermo", add_to = self.nodes, x=610, y=777)
        berlin = Node("Berlin", add_to = self.nodes, x=603, y=268)
        kobenhavn = Node("København", add_to = self.nodes, x=569, y=121)
        stockholm = Node("Stockholm", add_to = self.nodes, x=696, y=25)
        wien = Node("Wien", add_to = self.nodes, x=673, y=410)
        zagreb = Node("Zagreb", add_to = self.nodes, x=657, y=522)
        sarajevo = Node("Sarajevo", add_to = self.nodes, x=761, y=592)
        brindisi = Node("Brindisi", add_to = self.nodes, x=669, y=647)
        athina = Node("Athína", add_to = self.nodes, x=820, y=743)
        sofia = Node("Sofia", add_to = self.nodes, x=842, y=603)
        budapest = Node("Budapest", add_to = self.nodes, x=731, y=440)
        warszawa = Node("Warszawa", add_to = self.nodes, x=802, y=257)
        danzig = Node("Danzig", add_to = self.nodes, x=743, y=172)
        riga = Node("Rīga", add_to = self.nodes, x=843, y=61)
        petrograd = Node("Petrograd", add_to = self.nodes, x=1050, y=56)
        wilno = Node("Wilno", add_to = self.nodes, x=939, y=226)
        smolensk = Node("Smolensk", add_to = self.nodes, x=1065, y=232)
        kyiv = Node("Kyiv", add_to = self.nodes, x=987, y=322)
        moskva = Node("Moskva", add_to = self.nodes, x=1169, y=202)
        bucuresti = Node("București", add_to = self.nodes, x=917, y=525)
        sevastopol = Node("Sevastopol", add_to = self.nodes, x=1086, y=543)
        constantinople = Node("Constantinople", add_to = self.nodes, x=979, y=677)
        smyrna = Node("Smyrna", add_to = self.nodes, x=924, y=774)
        angora = Node("Angora", add_to = self.nodes, x=1073, y=743)
        erzurum = Node("Erzurum", add_to = self.nodes, x=1172, y=714)
        sochi = Node("Sochi", add_to = self.nodes, x=1194, y=560)
        rostov = Node("Rostóv", add_to = self.nodes, x=1201, y=451)
        kharkov = Node("Kharkov", add_to = self.nodes, x=1152, y=387)

        # Edges
        self.edges.append(Edge([lisbon, cadiz], Color.blue, 2, "#00be3a"))
        self.edges.append(Edge([lisbon, madrid], Color.pink, 3, "#63bc3a"))
        self.edges.append(Edge([cadiz, madrid], Color.orange, 3, "#008d39"))
        self.edges.append(Edge([madrid, barcelona], Color.yellow, 2, "#016d3b"))
        self.edges.append(Edge([madrid, pamplona], Color.black, 3, "#077b4c", track_type=TrackType.tunnel))
        self.edges.append(Edge([madrid, pamplona], Color.white, 3, "#004d39", track_type=TrackType.tunnel))
        self.edges.append(Edge([barcelona, pamplona], Color.grey, 2, "#07a163", track_type=TrackType.tunnel))
        self.edges.append(Edge([barcelona, marseille], Color.grey, 4, "#20e093"))
        self.edges.append(Edge([pamplona, marseille], Color.red, 4, "#4bfcb4"))
        self.edges.append(Edge([pamplona, paris], Color.blue, 4, "#21dfd3"))
        self.edges.append(Edge([pamplona, paris], Color.green, 4, "#4afcf0"))
        self.edges.append(Edge([pamplona, brest], Color.pink, 4, "#19c0b6"))
        self.edges.append(Edge([brest, paris], Color.black, 3, "#13a39a"))
        self.edges.append(Edge([brest, dieppe], Color.orange, 2, "#0d8178"))
        self.edges.append(Edge([paris, dieppe], Color.pink, 1, "#085d56"))
        self.edges.append(Edge([dieppe, london], Color.grey, 2, "#07435d", locomotive_count=1))
        self.edges.append(Edge([dieppe, london], Color.grey, 2, "#0d5c7d", locomotive_count=1))
        self.edges.append(Edge([dieppe, bruxelles], Color.green, 2, "#137099"))
        self.edges.append(Edge([london, amsterdam], Color.grey, 2, "#1316af", locomotive_count=2))
        self.edges.append(Edge([london, edinburgh], Color.black, 4, "#181bcc"))
        self.edges.append(Edge([london, edinburgh], Color.orange, 4, "#1a1de6"))
        self.edges.append(Edge([paris, bruxelles], Color.yellow, 2, "#1787b7"))
        self.edges.append(Edge([paris, bruxelles], Color.red, 2, "#1da0d8"))
        self.edges.append(Edge([bruxelles, amsterdam], Color.black, 1, "#0b0f8a"))
        self.edges.append(Edge([amsterdam, essen], Color.yellow, 3, "#2528f3"))
        self.edges.append(Edge([amsterdam, frankfurt], Color.white, 2, "#393dff"))
        self.edges.append(Edge([bruxelles, frankfurt], Color.blue, 2, "#0b0c66"))
        self.edges.append(Edge([paris, frankfurt], Color.white, 3, "#2473d0"))
        self.edges.append(Edge([paris, frankfurt], Color.orange, 3, "#3888e7"))
        self.edges.append(Edge([paris, zurich], Color.grey, 3, "#3cc4fe", track_type=TrackType.tunnel))
        self.edges.append(Edge([paris, marseille], Color.grey, 4, "#20b1f2"))
        self.edges.append(Edge([marseille, roma], Color.grey, 4, "#1b65bc", track_type=TrackType.tunnel))
        self.edges.append(Edge([marseille, zurich], Color.pink, 2, "#50a0ff", track_type=TrackType.tunnel))
        self.edges.append(Edge([zurich, venezia], Color.green, 2, "#1756a3", track_type=TrackType.tunnel))
        self.edges.append(Edge([zurich, munchen], Color.yellow, 2, "#0e4585", track_type=TrackType.tunnel))
        self.edges.append(Edge([munchen, venezia], Color.blue, 2, "#7e11ba", track_type=TrackType.tunnel))
        self.edges.append(Edge([venezia, roma], Color.black, 2, "#8810c7"))
        self.edges.append(Edge([frankfurt, munchen], Color.pink, 2, "#0a3466"))
        self.edges.append(Edge([frankfurt, essen], Color.green, 2, "#6265ff"))
        self.edges.append(Edge([frankfurt, berlin], Color.black, 3, "#8762ff"))
        self.edges.append(Edge([frankfurt, berlin], Color.red, 3, "#653aec"))
        self.edges.append(Edge([essen, berlin], Color.blue, 2, "#552ad9"))
        self.edges.append(Edge([essen, kobenhavn], Color.grey, 3, "#461dc4", locomotive_count=1))
        self.edges.append(Edge([essen, kobenhavn], Color.grey, 3, "#3c15b0", locomotive_count=1))
        self.edges.append(Edge([kobenhavn, stockholm], Color.yellow, 3, "#2f1289"))
        self.edges.append(Edge([kobenhavn, stockholm], Color.white, 3, "#200a5c"))
        self.edges.append(Edge([roma, palermo], Color.grey, 4, "#9a42ca", locomotive_count=1))
        self.edges.append(Edge([roma, brindisi], Color.white, 2, "#9310d8"))
        self.edges.append(Edge([palermo, brindisi], Color.grey, 3, "#a118ea", locomotive_count=1))
        self.edges.append(Edge([brindisi, athina], Color.grey, 4, "#d234ed", locomotive_count=1))
        self.edges.append(Edge([palermo, smyrna], Color.grey, 6, "#b723d1", locomotive_count=2))
        self.edges.append(Edge([sarajevo, athina], Color.green, 4, "#9f1cb6"))
        self.edges.append(Edge([sofia, athina], Color.pink, 3, "#b71a73"))
        self.edges.append(Edge([sarajevo, sofia], Color.grey, 2, "#9e1462", track_type=TrackType.tunnel))
        self.edges.append(Edge([zagreb, sarajevo], Color.red, 3, "#e75cff"))
        self.edges.append(Edge([sarajevo, budapest], Color.pink, 3, "#840f53"))
        self.edges.append(Edge([venezia, zagreb], Color.grey, 2, "#b336f4"))
        self.edges.append(Edge([munchen, wien], Color.orange, 3, "#8d3abc"))
        self.edges.append(Edge([wien, zagreb], Color.grey, 2, "#c65bff"))
        self.edges.append(Edge([zagreb, budapest], Color.orange, 2, "#5b0b6a"))
        self.edges.append(Edge([wien, budapest], Color.red, 1, "#720d83"))
        self.edges.append(Edge([wien, budapest], Color.white, 1, "#8c18a1"))
        self.edges.append(Edge([berlin, wien], Color.green, 3, "#7215a2"))
        self.edges.append(Edge([wien, warszawa], Color.blue, 4, "#690b40"))
        self.edges.append(Edge([berlin, warszawa], Color.pink, 4, "#510e75"))
        self.edges.append(Edge([berlin, warszawa], Color.yellow, 4, "#620f91"))
        self.edges.append(Edge([berlin, danzig], Color.grey, 4, "#3f0a5c"))
        self.edges.append(Edge([danzig, warszawa], Color.grey, 2, "#ae1f25"))
        self.edges.append(Edge([danzig, riga], Color.black, 3, "#88151a"))
        self.edges.append(Edge([stockholm, petrograd], Color.grey, 8, "#6e0f13", track_type=TrackType.tunnel))
        self.edges.append(Edge([riga, petrograd], Color.grey, 4, "#6f2910"))
        self.edges.append(Edge([riga, wilno], Color.green, 4, "#ea2d34"))
        self.edges.append(Edge([warszawa, wilno], Color.red, 3, "#ff565b"))
        self.edges.append(Edge([warszawa, kyiv], Color.grey, 4, "#fc52b3"))
        self.edges.append(Edge([budapest, kyiv], Color.grey, 6, "#e73299", track_type=TrackType.tunnel))
        self.edges.append(Edge([budapest, bucuresti], Color.grey, 4, "#c06d21", track_type=TrackType.tunnel))
        self.edges.append(Edge([sofia, bucuresti], Color.grey, 2, "#a85914", track_type=TrackType.tunnel))
        self.edges.append(Edge([sofia, constantinople], Color.blue, 3, "#8b490d"))
        self.edges.append(Edge([bucuresti, constantinople], Color.yellow, 3, "#9b7e00"))
        self.edges.append(Edge([athina, smyrna], Color.grey, 2, "#ce2485", locomotive_count=1))
        self.edges.append(Edge([smyrna, constantinople], Color.grey, 2, "#64350b", track_type=TrackType.tunnel))
        self.edges.append(Edge([smyrna, angora], Color.orange, 3, "#64530b", track_type=TrackType.tunnel))
        self.edges.append(Edge([constantinople, angora], Color.grey, 2, "#7b6300", track_type=TrackType.tunnel))
        self.edges.append(Edge([angora, erzurum], Color.black, 3, "#fece00"))
        self.edges.append(Edge([constantinople, sevastopol], Color.grey, 4, "#cea701", locomotive_count=2))
        self.edges.append(Edge([sevastopol, erzurum], Color.grey, 4, "#ebbe00", locomotive_count=2))
        self.edges.append(Edge([sochi, erzurum], Color.red, 3, "#ffde59", track_type=TrackType.tunnel))
        self.edges.append(Edge([sevastopol, sochi], Color.grey, 2, "#cadb00", locomotive_count=1))
        self.edges.append(Edge([rostov, sochi], Color.grey, 2, "#f2ff58"))
        self.edges.append(Edge([sevastopol, rostov], Color.grey, 4, "#a8b600"))
        self.edges.append(Edge([kharkov, rostov], Color.green, 2, "#889400"))
        self.edges.append(Edge([bucuresti, sevastopol], Color.white, 4, "#b99500"))
        self.edges.append(Edge([bucuresti, kyiv], Color.grey, 4, "#e58632"))
        self.edges.append(Edge([kyiv, kharkov], Color.grey, 4, "#fca659"))
        self.edges.append(Edge([kharkov, moskva], Color.grey, 4, "#fc855a"))
        self.edges.append(Edge([kyiv, smolensk], Color.red, 3, "#f25d25"))
        self.edges.append(Edge([wilno, kyiv], Color.grey, 2, "#cb2227"))
        self.edges.append(Edge([wilno, smolensk], Color.yellow, 3, "#9c3814"))
        self.edges.append(Edge([smolensk, moskva], Color.orange, 2, "#d35322"))
        self.edges.append(Edge([wilno, petrograd], Color.blue, 4, "#873110"))
        self.edges.append(Edge([petrograd, moskva], Color.white, 4, "#bc491d"))

        # Tickets
        self.tickets.append(Ticket(cadiz, stockholm, 21))  # NOTE: Check this one

