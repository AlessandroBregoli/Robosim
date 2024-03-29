import model

import draw
mappa = model.load_map("mappa_3.txt")
modello = model.Robosim_model(3, mappa, 0.5)
print("Mappa da esplorare:")
model.print_map(mappa)
modello.running = True
i = 0
while modello.running:
    i += 1
    modello.step()
    print("Iterazione: " + str(i))
    if i%10 == 0:
        model.print_map(modello.explored_map)
        draw.draw_map(modello,str(i)+".svg")
print(modello.datacollector.get_model_vars_dataframe())