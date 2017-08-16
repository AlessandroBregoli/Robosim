import model

mappa = model.load_map("mappa_1.txt")
modello = model.Robosim_model(2, mappa)
print("Mappa da esplorare:")
model.print_map(mappa)
for tmp in range(5):
    print("20 iterazioni:")
    for x in range(20):
        modello.step()
    model.print_map(modello.explored_map)
