class Graphium::AnalyticsController < ApplicationController
    respond_to :json, :html, :js
    
    def index
        
    end
    
    def getAgentsActives
        @analytics_agent = Graphium::AgentStory.where(:active => true).all
        #@analytics_agent = Graphium::AgentStory.all
        respond_to do |format|
          format.json { render :json => @analytics_agent }
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
