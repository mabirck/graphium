# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).
#
# Examples:
#
#   cities = City.create([{ name: 'Chicago' }, { name: 'Copenhagen' }])
#   Mayor.create(name: 'Emanuel', city: cities.first)
User.create(:email=>"admin@graphium.com",:password => "30271255", :password_confirmation => "30271255", :first_name => "Administrador", :last_name => "do Sistema")

if Graphium::Configuration.all.length != 0
        Graphium::Configuration.delete_all
end
Graphium::Configuration.create( :swarm_agent_number => 3, :swarm_agent_names_API => "http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all", :swarm_agent_names =>['Coralina Malaya','Abigail Johnson','Antonietta Marinese','Elisa Rogoff','Serafim Folkerts','Dulce Barrell'], :mongo_db => "graphium",:mongo_host =>"localhost",:mongo_port =>27017, :swarm_agent_colors => ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"],:inf_positive => 99999, :inf_negative => -99999, :osmapi_user => "glaucomunsberg",:osmapi_password =>"30271255")
