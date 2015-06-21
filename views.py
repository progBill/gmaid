from flask import Flask, render_template, jsonify, Blueprint
from static import queries
from random import choice, randint, sample
from json import dumps
from npc import NPC 

app = Flask(__name__)
db = queries.Database()

@app.route("/")
def home():
    return render_template('ang.html')

@app.route("/getname")
@app.route("/getname/<numDudes>")
def getName(numDudes=10):
    npc_results = []

    # first, create all the NPCs
    for npc in db.get_npc_base():
        npc_results.append( NPC(npc[0],npc[1],npc[2],npc[3]))

    npcs = []
    for i in range(int(numDudes)):
        npcs.append(choice(npc_results))

    # get possible professions for our NPCs
    professions = {}
    profession_distribution = []
    for profession in db.get_all_professions():
        professions[profession[4]] = {'occupation':profession[0], 'description':profession[1], 'category':profession[2]}
        # each entry increases likelihood of profession appearing
        profession_distribution.extend( [profession[4] for x in range(profession[3])] )

    # give jobs to the NPCs
    for npc in npcs:
        #get random profession based on rarity
        new_job = choice(profession_distribution)
        # lower the chances of getting the same job again
        for x in range(2):
            if new_job in profession_distribution: 
                profession_distribution.remove(new_job)
        #assign profession to NPC
        npc.profession = professions[new_job]

    # give traits to NPCs
    traits = db.get_all_traits()
    for npc in npcs:
        npc.traits = [choice(traits)[0], choice(traits)[0], choice(traits)[0]]

    # figure out how to jsonify the list of NPCs
    npc_return = '{' + ','.join([ '"' + str(w) + '":' + x.__str__() for w, x in enumerate(npcs)]) + '}'
    return npc_return

@app.route("/gettown")
def getTown():
    places = choice(db.get_all_places())
    return dumps({"town":places})

if __name__ == '__main__':
    app.run(debug=True)

