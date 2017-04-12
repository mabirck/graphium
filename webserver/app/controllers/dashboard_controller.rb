class DashboardController < ApplicationController
    
    before_filter :authenticate_user!
    layout "inside"
    def index
        
        
        @swarms_actives = Graphium::Swarm.where(:active => true, :user_email => current_user.email).all
        if not user_signed_in?
			redirect_to url_for(:controller => :application, :action => :index)
		else
            render 'index.html.erb'
        end
    end
end
