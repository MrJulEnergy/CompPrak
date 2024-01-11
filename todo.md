# Todolist

- [ ] Periodic Boundary Conditions (wenn das gewünscht ist. ich fände es sehr cool)
- [ ] Aspect Ratio reparieren in der transform_coords method (absoluter krampf aber vielleicht können mathematiker da besser drüber nachdenken als ich.)
- [x] Warum sieht es so aus als würden die variabelen Temp, mass und gamma keinen Einfluss auf die simulation haben?
    - LÖSUNG: Funktioniert doch, sah nur so aus bei variabler Boundary. Wenn die konstant für verschiedene Variablen getestet wird, sieht es wieder gut aus
- [ ] Leader Force erstellen (kraft die richtung leader zeigt (z.b. LJ-Potential oder Coulomb-Kraft wären gute kandidaten dafür (letzteres ist besser, da langreichweitende kraft, aber dann dürfen keine periodic boundaries mehr verwendet werden)))
    - Verlet lists?
    - cell lists?
- [ ] Trajektorie des leader vorgeben
- [ ] Farben der parikel variable machen
- [ ] dt=fps ist blöd. zu viele fps bei kleinem dt sind nicht gut für den computer. => fps und dt entkoppelen und stridelenght einführen (es werden nur alle paar schritte werte aus der simulation abgespeichter für die animation)