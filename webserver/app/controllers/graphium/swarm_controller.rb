require 'net/http'

class Graphium::SwarmController < ApplicationController
    
    layout "inside"
    before_filter :authenticate_user!
    respond_to :json, :html, :js
    
    def index
        @swarms = Graphium::Swarm.all #where({'active': true})
        @swarm_actives = Graphium::Swarm.where({'active': true,'user_email': current_user.email})
    end
    
    def launcher
        @swarms = Graphium::Swarm.where({'active': true,'user_email': current_user.email})
    end
    
    def startSwarm
        
        

        name = params[:swarm_name]
        name = name.gsub(" ","_")
        
        swarm = Graphium::Swarm.new
        swarm.identifier                = params[:swarm_identifier]
        swarm.name                      = name
        swarm.user_email                = current_user.email
        swarm.active                    = true
        swarm.seconds_to_check_agents   = params[:swarm_turns].to_i
        swarm.city_id                   = params[:swarm_city]
        swarm.num_agent                 = params[:swarm_num_agent].to_i
        swarm.cycles                    = params[:swarm_agent_cycles].to_i
        swarm.logs                      = []
        swarm.start_at                  = Time.now.strftime('%Y-%m-%d %H:%M:%S')
        swarm.save
        
        locations = []
        
        if params[:swarm_wish_list]
            locations_from_params = params[:swarm_wish_list].split(':')
            locations_from_params.each do |each_location|
                lat_lng = each_location.split(',')
                if lat_lng.length == 2
                    
                    wishlist                    = Graphium::Wishlist.new
                    wishlist.lat                = lat_lng[0].to_f
                    wishlist.lng                = lat_lng[1].to_f
                    wishlist.swarm_identifier   = swarm.identifier
                    wishlist.user_email         = current_user.email
                    wishlist.dt_required        = Time.now.strftime('%Y-%m-%d %H:%M:%S')
                    wishlist.processed          = false
                    wishlist.city_id            = params[:swarm_city]
                    wishlist.priority           = 1.0
                    
                    url = URI.parse("http://nominatim.openstreetmap.org/reverse?&format=json&lat=#{lat_lng[0]}&lon=#{lat_lng[1]}")
                    req = Net::HTTP::Get.new(url.to_s)
                    res = Net::HTTP.start(url.host, url.port) {|http|
                      http.request(req)
                    }
                    logger.info 'API NOMINATIM'
                    logger.info "http://nominatim.openstreetmap.org/reverse?&format=json&lat=#{lat_lng[0]}&lon=#{lat_lng[1]}"
                    json_result = JSON.parse(res.body) 
                    if json_result.key?("osm_id")
                        wishlist.osm_way_id = json_result['osm_id'].to_i
                        if json_result.key?("address") and json_result['address'].key?("road")
                            wishlist.address = json_result['address']['road']
                        end
                        
                    end
                    
                    wishlist.save
                    
                end
            end
        end
        logger.info 'Inicialize the swarm'
        Thread.new do
            logger.info 'Start thread'
            logger.info system( "python ../swarm/Main.py -i #{params[:swarm_identifier]}" )
        end
        @output = true
        respond_to do |format|
          format.json { render :json => {"output" => @output} }
        end
    end
end
