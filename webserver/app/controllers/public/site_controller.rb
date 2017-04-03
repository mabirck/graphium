class Public::SiteController < ApplicationController
    
    respond_to :json, :html, :js
    layout "outside"
    
    def index
        if user_signed_in?
			if params[:homepage] == nil
				redirect_to "/dashboard"
			else
				@resource = User.new
				respond_with(@resource)
			end
		else
			@resource = User.new
			respond_with(@resource)
		end
    end
end
