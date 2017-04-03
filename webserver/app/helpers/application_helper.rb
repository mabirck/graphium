module ApplicationHelper
    
    def form_save_btn submit
        returned = "<div class='row'><div class='col s12'><a class='waves-effect waves-light btn' style='background-color: #e4e4e4;color: black;' onClick='window.history.back()'>Back</a>"
        returned +=  submit
        returned += "</div></div>
                     <script>
                        $(document).ready(function(){
                            $(\"input[type='submit']\").addClass('btn waves-effect waves-light');
                            $(\"input[type='submit']\").css('margin-left','10px');
                        })
                     </script>"
        returned.html_safe
    end
    
    def breadcrumbs elements = [{:name => 'Home',:path => '/'},{:name => 'Dashboard',:path => '/dashboard'}], id=nil, editing=false
        
        returned = "<nav id='breadcrumb'  class='unselectable' style='background-color:white;margin-left: 60px !important;'>
                        <div class='nav-wrapper'>
                            <div class='col s12'>"
                                elements.each do |element|
                                    returned += "<a href='#{element[:path]}' class='breadcrumb'>#{element[:name]}</a>"
                                end
                                if id != nil
                                    returned += "<a class='breadcrumb' style='cursor: default;'>#{id}</a>"
                                end
                                if editing != false
                                    returned += "<a class='breadcrumb' style='cursor: default;'>edit</a>"
                                end
        returned += "       </div>
                        </div>
                    </nav>
                    <style>
                        #breadcrumb{
                            box-shadow: none
                        }
                        .breadcrumb{
                            color:black
                        }
                        .breadcrumb:before{
                            color:black
                        }
                        .breadcrumb:last-child{
                            color:black
                        }
                    </style>"
        
        value_to_set = returned.html_safe
        returned = "<script>
                        $(document).ready(function(){
                            $('#controllers').html(`#{value_to_set}`)
                        });
                    </script>"
        returned.html_safe
    end
end
