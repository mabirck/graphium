class Graphium::AnalyticsController < ApplicationController
    respond_to :json, :html, :js
    layout "inside"
    def index
        
    end
    
    def getSwarmActive
        @analytics = {}
        @analytics['swarm'] = nil
        @analytics['agents'] = []
        @analytics['swarm'] = Graphium::Swarm.where(:active => true, :user_email => current_user.email).first
        if @analytics['swarm'] != nil
            @analytics['agents'] = Graphium::Agent.where(:swarm_identifier => @analytics['swarm'].identifier )
        end
        #@analytics_agent = Graphium::AgentStory.all
        respond_to do |format|
          format.json { render :json => @analytics }
        end
    end
    
    def history
        @swarms = Graphium::AgentStory.distinct('swarm_identifier')
    end
    
    def getAgentsBySwarm
        @analytics_agent = Graphium::AgentStory.where(:swarm_identifier => params[:swarm_identifier]).all
        #@analytics_agent = Graphium::AgentStory.all
        respond_to do |format|
          format.json { render :json => @analytics_agent }
        end
    end
end
