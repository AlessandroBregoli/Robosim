import model

mappa = model.load_map("mappa_1.txt")
modello = model.Robosim_model(3, mappa)
print("Mappa da esplorare:")
model.print_map(mappa)
modello.running = True
while modello.running:
    modello.step()
print(modello.datacollector.get_model_vars_dataframe())
