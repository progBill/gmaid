from flask import (Flask, render_template, request)
from static import queries
from random import choice, randrange
from json import dumps, loads
from npc import NPC
from Building import Building

app = Flask(__name__)
db = queries.Database()

@app.route("/")
def home():
    return render_template('ang.html')

def get_npc(numDudes):
    # handle request data
    req_data = loads(request.data)
    culture_filters = {}
    if 'cultureFilter' in req_data:
        culture_filters = req_data['cultureFilter']
    blank_npcs = assemble_npc_list(numDudes, culture_filters)
    npcs = jobs_for_npcs(blank_npcs)
    # give traits to NPCs
    traits = db.get_all_traits()
    for npc in npcs:
        npc.traits = [choice(traits)[0], choice(traits)[0], choice(traits)[0]]

    # figure out how to jsonify the list of NPCs
    npc_return = '{' + ','.join([ '"' + str(x) + '":' + y.__str__() for x, y in enumerate(npcs)]) + '}'
    return npc_return

@app.route("/gettown")
@app.route("/gettown/<numDudes>", methods=['POST','GET'])
def getTown(numDudes=10):
    # handle request data
    req_data = loads(request.data)
    culture_filters = {}

    print req_data

    if 'cultureFilter' in req_data: culture_filters = req_data['cultureFilter']
    if 'size' in req_data: size = req_data['size'] * 10

    # get the population of the town
    json_npcs = loads(get_npc( numDudes ))
    npcs = []
    for x in json_npcs:
        pc = json_npcs[x]
        dude = NPC(pc['first'], pc['last'], pc['sex'], pc['culture'])
        dude.profession = pc['profession']
        dude.traits = pc['traits']
        npcs.append( dude )

    # stuff all professions in a dict,
    professions = {}
    profession_distribution = []
    for profession in db.get_all_professions():
        professions[profession[4]] = {'occupation':profession[0], 'description':profession[1], 'category':profession[2], 'id':profession[4]}

    # load all possible buildings to get started actualizing our new Town
    buildings_raw = []
    for bld in db.get_all_businesses():
        buildings_raw.append( Building(bld[2], bld[4], bld[5]) )

    # pull out the buildings actually in our town, based on size
    buildings = []
    for i, bld in enumerate(buildings_raw):
        #print '\nbld: {}\nsize: {}\nreqPop: {}\nnumThere: {}'.format(bld.name, size, bld.reqPopulation, size / bld.reqPopulation)
        for x in range( size / bld.reqPopulation ):
            # need to reinstantiate so each instance has its own worker
            this_building = Building(bld.name, bld.reqPopulation, bld.requiredProfession)

            # get an employee for the business
            worker = npcs.pop()
            worker.profession = professions[bld.requiredProfession]
            this_building.worker = worker.__dict__
            buildings.append(this_building)

    # build the final town product
    retTown = {} # the thing to jsonify and return
    bld = {} # buildings dict
    retTown["name"] = choice(db.get_all_places())[0]
    # put buildings in dict for easy jsonify
    for x,y in enumerate(buildings):
        bld[x] = y.__dict__
    retTown['buildings'] = bld
    # populate town with NPCs
    retTown['npcs'] = [n.__dict__ for n in npcs]
    return dumps(retTown)

@app.route("/getbusinesses", methods=['POST','GET'])
def get_businesses():
    return dumps({"businesses":db.get_all_businesses()})


################################
#  Utility functions
################################

def assemble_npc_list(numDudes, culture_filters):
    # set up the where clause for the culture filters
    cultures_result = db.get_all_cultures()
    cultures = dict((y.lower(), str(x)) for x,y in cultures_result)
    culture_clause = []
    where_clause = ""
    if 'cultureFilter' in culture_filters:
        for k in culture_filters['cultureFilter'].keys():
            if culture_filters['cultureFilter'][k] == True:
                culture_clause.append(cultures[k])

    if culture_clause:
        culture_where = "culture IN ('" + "','".join(culture_clause) + "')"
        where_clause = "WHERE {}".format(culture_where)

    # create all the NPCs
    npc_results = []
    for npc in db.get_npc_base(where_clause):
        npc_results.append( NPC(npc[0],npc[1],npc[2],npc[3]))
    npcs = []
    for i in range(int(numDudes)):
        npcs.append(choice(npc_results))

    return npcs

def jobs_for_npcs(npcs):
    # get possible professions for our NPCs
    professions = {}
    profession_distribution = []
    for profession in db.get_all_professions():
        professions[profession[4]] = {'occupation':profession[0], 'description':profession[1], 'category':profession[2], 'id':profession[4]}
        # each entry increases likelihood of profession appearing
        profession_distribution.extend( [profession[4] for x in range(profession[3])] )

    # give jobs to the NPCs
    # TODO: deal with what happens when there are more NPCs than jobs
    for npc in npcs:
        #get random profession based on rarity
        new_job = choice(profession_distribution)
        # lower the chances of getting the same job again
        for x in range(2):
            if new_job in profession_distribution:
                profession_distribution.remove(new_job)
        #assign profession to NPC
        npc.profession = professions[new_job]

    return npcs


if __name__ == '__main__':
    app.run(debug=True)
