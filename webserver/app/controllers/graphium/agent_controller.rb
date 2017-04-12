class Graphium::AgentController < ApplicationController
    
    layout "inside"
    before_filter :authenticate_user!
    def index
        @agents = Graphium::Agent.all#where({'active': true})
    end
end
