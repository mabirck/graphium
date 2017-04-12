class Graphium::AnalyticsController < ApplicationController
    respond_to :json, :html, :js
    before_filter :authenticate_user!
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
        @swarms = Graphium::Swarm.where(:active => false).all
    end
    
    def getSwarmAndAgents
        @analytics = {}
        @analytics['swarm'] = nil
        @analytics['agents'] = []
        @analytics['swarm'] = Graphium::Swarm.where(:identifier => params[:swarm_identifier]).first
        if @analytics['swarm'] != nil
            @analytics['agents'] = Graphium::Agent.where(:swarm_identifier => @analytics['swarm'].identifier )
        end
        #@analytics_agent = Graphium::AgentStory.all
        respond_to do |format|
          format.json { render :json => @analytics }
        end
    end
    
    def finishSwarm
        @swarm = Graphium::Swarm.where(:identifier => params[:swarm_identifier]).first
        if @swarm
            @swarm.active = false
            if @swarm.save
                respond_to do |format|
                  format.json { render :json => true }
                end
            else
                respond_to do |format|
                  format.json { render :json => false }
                end
            end
        else
            respond_to do |format|
              format.json { render :json => false }
            end
        end
    end
end
