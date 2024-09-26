
#------------------------------------------------To Import--------------------------------------------

from flask import Flask, render_template, request
from flask import current_app as app
from datetime import datetime
from flask import session
from flask import redirect, url_for
from backend.models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#------------------------------------------------To Import--------------------------------------------





















#----------------------------------------------------------Influencer-Start------------------------------------------------------------------------------------------------------- 














@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname=request.form.get("username")
        pwd=request.form.get("password")
        usr = Influencer.query.filter_by(username=uname, password=pwd).first()
        if usr:
           session['uname'] = uname
           lusr = Influencer.query.filter_by(
               username=uname).first()
           i_id = lusr.influencer_id
           session['i_id'] = i_id
          
           
            
           return redirect(url_for('home'))
        else:
            return render_template("user_login.html",msg="invalid")      
    return render_template("user_login.html")





@app.route("/home", methods=["GET","POST"])
def home():
        uname = session.get("uname")
        usr = Influencer.query.filter_by(username = uname).first()
        i_id = usr.influencer_id
        if usr.status =='flagged':
            msg ='You have been FLAGGED ! by ADMIN'
        else: msg = ''
        revenue = []
        p_ads = db.session.query(Ads, Sponsor, Campaigns).filter(Ads.influencer_id == i_id, Ads.status == 'pending').join(
            Sponsor, Ads.sponsor_id == Sponsor.sponsor_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).filter(Campaigns.visibility == "public").all()
           
        a_ads = db.session.query(Ads, Sponsor, Campaigns).filter(Ads.influencer_id == i_id, Ads.status == 'accepted').join(
               Sponsor, Ads.sponsor_id == Sponsor.sponsor_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).all()
        c_ads = db.session.query(Ads, Sponsor, Campaigns).filter(Ads.influencer_id == i_id, Ads.status == 'completed').join(
               Sponsor, Ads.sponsor_id == Sponsor.sponsor_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).all()
           
        ta_ads = Ads.query.filter(Ads.influencer_id == i_id, (Ads.status == 'accepted') | (
            Ads.status == 'completed')).all()
        for i in ta_ads:
            revenue.append(int(i.payment))
        Rtotal = sum(revenue)
        plength = len(p_ads)
        alength = len(ta_ads)
        rating = 0

        if alength < 1:
               rating = 0
        elif alength >= 1 and alength <2:
               rating = 3.2
        elif alength >= 2 and alength <4:
               rating = 4.5
        elif alength >= 4:
               rating = 5.0

        usr.ratings = rating
        db.session.commit()
        
           
        return render_template("user_dash.html", uname=uname,p_ads=p_ads, a_ads=a_ads,c_ads = c_ads, Rtotal = Rtotal, plength = plength,msg =msg, alength = alength,rating = rating, influencer_id = i_id)




@app.route("/user_register", methods=["GET","POST"])
def user_register():
    if request.method=="POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        cat=request.form.get("category")
        wb=request.form.get("website")
        pt=request.form.get("platform")
        fw=request.form.get("reach")
        usr = Influencer.query.filter_by(username=uname).first()
        if not usr:
          new_usr = Influencer(username=uname,password=pwd,category=cat,website=wb,platform=pt, reach = fw, status = 'unflagged')
          db.session.add(new_usr)
          db.session.commit()
          return render_template("user_login.html",msg="")
        else:
         return render_template("user_register.html",msg="Sorry, dont joke")

    return render_template("user_register.html", msg="")


@app.route("/iaccept_ad/<int:ad_id>", methods=["GET", "POST"])
def accept_ad(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        ads.status = "accepted"
        db.session.commit()

    return redirect('/home')


@app.route("/ireject_ad/<int:ad_id>", methods=["GET", "POST"])
def reject_ad(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        ads.status = "rejected"
        db.session.commit()

    return redirect('/home')


@app.route("/camp_select", methods=["GET", "POST"])
def camp_select():
    ad = Ads.query.all()
    uname = session.get('uname')
    usr = Influencer.query.filter_by(username=uname).first()
    i_id = usr.influencer_id
    p_ads = db.session.query(Ads, Sponsor, Campaigns).filter(Ads.status == 'pending', Ads.influencer_id == None).join(
        Sponsor, Ads.sponsor_id == Sponsor.sponsor_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).filter(Campaigns.visibility == "public").all()

    return render_template("camp_search.html", p_ads=p_ads, i_id=i_id)


@app.route("/request_ad/<int:ad_id>", methods=["GET", "POST"])
def request_ad(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        uname = session.get('uname')
        usr = Influencer.query.filter_by(username=uname).first()
        i_id = usr.influencer_id
      
        ads.status = "requested"
        ads.influencer_id = i_id
        db.session.commit()

    return redirect('/home')


@app.route("/ad_done/<int:ad_id>", methods=["GET", "POST"])
def ad_completed(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        ads.status = "completed"
        db.session.commit()

    return redirect('/home')


@app.route("/user_profile/<int:influencer_id>", methods=["GET", "POST"])
def user_profile(influencer_id):
    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("password")
        category = request.form.get("category")
        website = request.form.get("website")
        platform = request.form.get("platform")
        reach = request.form.get("reach")
        usr = Influencer.query.filter_by(influencer_id=influencer_id).first()
        # -------------

        usr.password = password
        usr.category = category
      
        usr.website = website
        usr.platform = platform
        usr.reach = reach
        db.session.commit()

        influencer = Influencer.query.filter_by(
            influencer_id=influencer_id).first()
        return render_template("user_profile.html", influencer=influencer, msg="Changes saved to the Database!")

    influencer = Influencer.query.filter_by(
        influencer_id=influencer_id).first()
    return render_template("user_profile.html", influencer=influencer, msg=" no updates ")


@app.route("/remove_influencer/<int:influencer_id>")
def remove_influencer(influencer_id):
    usr = Influencer.query.get(influencer_id)

    ads = Ads.query.filter_by(influencer_id=influencer_id).all()

    if ads:
        for ad in ads:
            db.session.delete(ad)
    db.session.delete(usr)

    db.session.commit()

    return redirect('/')





#----------------------------------------------------------Influencer-End------------------------------------------------------------------------------------------------------- 



































#----------------------------------------------------------Brand-Start------------------------------------------------------------------------------------------------------- 










@app.route("/brand_home", methods=["GET","POST"])
def brand_home():
   
        
        sname = session.get('sname')
        spon = Sponsor.query.filter_by(username = sname).first()
        if spon.status == 'flagged':
            msg = "You have been Flagged by Admin"
        else: msg=''
            
            
        s_id = spon.sponsor_id
        
        r_ads = db.session.query(Ads, Influencer, Campaigns).filter(Ads.sponsor_id == s_id, Ads.status == 'requested').join(
               Influencer, Ads.influencer_id == Influencer.influencer_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).all()
        
        a_ads = db.session.query(Ads, Influencer, Campaigns).filter(Ads.sponsor_id == s_id, Ads.status == 'accepted').join(
               Influencer, Ads.influencer_id == Influencer.influencer_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).all()
        c_ads = db.session.query(Ads, Influencer, Campaigns).filter(Ads.sponsor_id == s_id, Ads.status == 'completed').join(
               Influencer, Ads.influencer_id == Influencer.influencer_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).all()
        ta_ads = Ads.query.filter(Ads.sponsor_id == s_id,(Ads.status == 'accepted') | (Ads.status == 'completed')).all()
        spending = []
        for i in ta_ads:
            spending.append(int(i.payment))
        Rtotal = sum(spending)
        rlength = len(r_ads)
        alength = len(ta_ads)
        clength = len(c_ads)
        
        return render_template("brand_dash.html", sname=sname,r_ads=r_ads, a_ads=a_ads,msg=msg, c_ads = c_ads,sponsor_id = s_id, Rtotal = Rtotal, plength = rlength, alength= alength,clength = clength)
        

    

@app.route("/brand_register", methods=["GET", "POST"])
def brand_register():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        loc = request.form.get("country")
        cat = request.form.get("category")
        wb = request.form.get("website")
        bname = request.form.get("bname")
        spending = request.form.get("spending")
        usr = Sponsor.query.filter_by(username=uname).first()
        if not usr:
          new_usr = Sponsor(username=uname, password=pwd,category=cat,web=wb,country=loc,bname=bname,spending = spending, status = 'unflagged')
          db.session.add(new_usr)
          db.session.commit()
          return render_template("brand_login.html", msg="")
        else:
         return render_template("brand_register.html", msg="Sorry, dont joke")

    return render_template("brand_register.html", msg="")


@app.route("/brand_login", methods=["GET", "POST"])
def brand_login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        usr = Sponsor.query.filter_by(username=uname, password=pwd).first()
        
        if usr:
            session['sname'] = uname
            lusr = Sponsor.query.filter_by(username=uname).first()
            s_id = lusr.sponsor_id
            session['s_id'] = s_id
           
            return redirect(url_for('brand_home'))

        else:
            return render_template("brand_login.html", msg="invalid")
    return render_template("brand_login.html")
    
    
@app.route("/new_camp", methods=["GET", "POST"])
def new_camp():
    sid = session.get('s_id')
    if request.method == "POST":
        name = request.form.get("title")
        desc = request.form.get("description")
        goals = request.form.get("goals")
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        sdate = datetime.strptime(sdate, "%Y-%m-%d")
        edate = datetime.strptime(edate, "%Y-%m-%d")
        bgt = request.form.get("budget")
        sname = session.get('sname')
        camp = Campaigns.query.filter_by(name=name).first()
        spon = Sponsor.query.filter_by(username=sname).first()
        sid = spon.sponsor_id
        session['s_id'] = sid
    

        if not camp:
          ncamp = Campaigns(name=name, description=desc,
                            goals=goals, start_date=sdate, end_date=edate, budget=bgt, sponsor_id=sid, visibility="public")
          db.session.add(ncamp)
          db.session.commit()
          campaigns = Campaigns.query.filter_by(sponsor_id=sid).all()

          return render_template("cam_dash.html", campaigns=campaigns, uname=sname, sid=sid)
        else:
         return render_template("cam_dash.html", msg="Sorry, dont joke", sid=sid)


    sname = session.get('sname')
    spon = Sponsor.query.filter_by(username=sname).first()
    sid = spon.sponsor_id
    session['s_id'] = sid
    campaigns = Campaigns.query.filter_by(sponsor_id=sid).all()

    return render_template("cam_dash.html", campaigns=campaigns, uname=sname, sid=sid)


@app.route("/ad_dash/<int:campaign_id>", methods=["GET", "POST"])
def ad_dash(campaign_id):
    ad = Ads.query.filter_by(campaign_id=campaign_id).all()
    s_id = session.get('s_id')

    session["camp_id"] = campaign_id
    return render_template("ad_dash.html", ads=ad, campaign_id=campaign_id, s_id=s_id)


@app.route("/new_ad/<int:campaign_id>", methods=["GET", "POST"])
def new_ad(campaign_id):
    camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
    cname = camp.name
    s_id = session.get('s_id')
    if request.method == "POST":
        aname = request.form.get("aname")
        terms = request.form.get("terms")
        payment = request.form.get("payment")
        ad = Ads.query.filter_by(name=aname).first()
        s_id = session.get('s_id')

        if not ad:
          nad = Ads(name=aname,
                    payment=payment, requirements=terms, sponsor_id=s_id, campaign_id=campaign_id, status="pending")

          db.session.add(nad)
          db.session.commit()
          ads = Ads.query.all()
          return redirect(url_for('ad_dash', campaign_id=campaign_id))
        else:
         return redirect(url_for('ad_dash', campaign_id=campaign_id))

    ads = Ads.query.all()

    return render_template("new_ad.html", campaign_id=campaign_id, cname=cname, s_id=s_id)


@app.route("/new_ad/<int:campaign_id>/<int:influencer_id>", methods=["GET", "POST"])
def ad_done(campaign_id, influencer_id):
    camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
    cname = camp.name
    usr = Influencer.query.filter_by(influencer_id=influencer_id).first()
    iname = usr.username

    if request.method == "POST":
        aname = request.form.get("aname")
        terms = request.form.get("terms")
        payment = request.form.get("payment")
        ad = Ads.query.filter_by(name=aname).first()
        s_id = session.get('s_id')

        if not ad:
          nad = Ads(name=aname,
                    payment=payment, requirements=terms, influencer_id=influencer_id, sponsor_id=s_id, campaign_id=campaign_id, status="pending")

          db.session.add(nad)
          db.session.commit()
          ads = Ads.query.all()
          return redirect(url_for('ad_dash', campaign_id=campaign_id))
        else:
         return redirect(url_for('ad_dash', campaign_id=campaign_id))

    ads = Ads.query.all()
    return render_template("ad_done.html", campaign_id=campaign_id, influencer_id=influencer_id, ads=ads, cname=cname, iname=iname)


@app.route("/search_user/<int:campaign_id>", methods=["GET", "POST"])
def find_user(campaign_id):
    if request.method == "POST":
        name = request.form.get("username")
        reach = request.form.get("reach")
        category = request.form.get("category")
       

        influencers = Influencer.query.filter((Influencer.reach == reach) | (
            Influencer.category == category) | (Influencer.username == name)).all()

        return render_template("user_done.html", influencers=influencers, campaign_id=campaign_id)
    influencers = Influencer.query.all()
    return render_template("user_search.html", campaign_id=campaign_id, influencers = influencers)


@app.route("/baccept_ad/<int:ad_id>", methods=["GET", "POST"])
def baccept_ad(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        ads.status = "accepted"
        db.session.commit()

    return redirect('/brand_home')


@app.route("/breject_ad/<int:ad_id>", methods=["GET", "POST"])
def breject_ad(ad_id):
    if request.method == "POST":
        ads = Ads.query.filter_by(ad_id=ad_id).first()
        ads.status = "rejected"
        db.session.commit()

    return redirect('/brand_home')


@app.route("/brand_profile/<int:sponsor_id>", methods=["GET", "POST"])
def brand_profile(sponsor_id):
    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("password")
        country = request.form.get("country")
        category = request.form.get("category")
        website = request.form.get("website")
        bname = request.form.get("bname")
        spending = request.form.get("spending")
        usr = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()

        usr.password = password
        usr.category = category

        usr.web = website
        usr.country = country
        usr.bname = bname
        usr.spending = spending
        db.session.commit()
        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
        return render_template("brand_profile.html", sponsor=sponsor, msg="Changes saved to the Database!")

    sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
    return render_template("brand_profile.html", sponsor=sponsor, msg="No updates")


@app.route("/ad_profile/<int:ad_id>", methods=["GET", "POST"])
def ad_profile(ad_id):
    if request.method == "POST":
        aname = request.form.get("aname")
        requirement = request.form.get("requirement")
        payment = request.form.get("payment")
        status = request.form.get("status")

        ad = Ads.query.filter_by(ad_id=ad_id).first()
        campaign_id = ad.campaign_id

        ad.requirements = requirement
        ad.payment = payment
        ad.status = status
        db.session.commit()
        ad = Ads.query.filter_by(ad_id=ad_id).first()
        return redirect(url_for('ad_dash', ad=ad, campaign_id=campaign_id, msg="Changes saved to the Database!"))

    ad = Ads.query.filter_by(ad_id=ad_id).first()
    return render_template("ad_profile.html", ad=ad, msg="No updates")


@app.route("/ad/delete/<int:ad_id>", methods=["GET", "POST"])
def del_ad(ad_id):
    ad = Ads.query.filter_by(ad_id=ad_id).first()

    db.session.delete(ad)
    db.session.commit()

    return redirect(url_for('new_camp'))


@app.route("/camp_profile/<int:campaign_id>", methods=["GET", "POST"])
def camp_profile(campaign_id):
    if request.method == "POST":
        desc = request.form.get("desc")
        goal = request.form.get("goal")
        budget = request.form.get("budget")
        vissibilty = request.form.get("visibility")

        camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
        camp.description = desc
        camp.goal = goal
        camp.budget = budget
        camp.visibility = vissibilty
        db.session.commit()
        camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
        return render_template("camp_profile.html", camp=camp, msg="Changes saved to the Database!")

    camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
    return render_template("camp_profile.html", camp=camp, msg="No updates")


@app.route("/camp/delete/<int:campaign_id>", methods=["GET", "POST"])
def del_camp(campaign_id):
    camp = Campaigns.query.filter_by(campaign_id=campaign_id).first()
    for ad in camp.ads:
        db.session.delete(ad)
    db.session.delete(camp)
    db.session.commit()

    return redirect(url_for('new_camp'))


@app.route("/remove_sponsor/<int:sponsor_id>")
def remove_spon(sponsor_id):
    spon = Sponsor.query.get(sponsor_id)
    ads = Ads.query.filter_by(sponsor_id=sponsor_id).all()
    camp = Campaigns.query.filter_by(sponsor_id=sponsor_id).all()
    db.session.delete(spon)
    if ads:
        for ad in ads:
            db.session.delete(ad)
    if camp:
        for cam in camp:
            db.session.delete(cam)

    db.session.commit()

    return redirect('/brand_login')






    
#----------------------------------------------------------Brand-End------------------------------------------------------------------------------------------------------- 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#----------------------------------------------------------Admin-Start------------------------------------------------------------------------------------------------------- 
    
    


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
        usr = Admin.query.filter_by(username=uname, password=pwd).first()
        if usr:
            a_id = usr.admin_id
            session["a_id"] = a_id
            session["aname"] = uname
          
            
            return redirect(url_for('admin_home'))
        else:
            return render_template("admin_login.html", msg="invalid")
    return render_template("admin_login.html")
    
@app.route("/admin_home")
def admin_home():
    
    uname =session.get('aname')
    sponsor = Sponsor.query.all()
    total_spon = Sponsor.query.count() 
   
    influencer = Influencer.query.all()
    total_usr = Influencer.query.count()
 
    ai_ads = Influencer.query.filter(
        Influencer.ads.any(Ads.status == "accepted")).all()
    campaign = Campaigns.query.filter_by(visibility="public").all()
    total_camp = Campaigns.query.filter_by(visibility="public").count()
  
    
    total_aads =   Ads.query.filter_by(status="accepted").count() 
  
    total_cads =  Ads.query.filter_by(status="completed").count() 
  
    total_rads = Ads.query.filter_by(status="rejected").count()
    
    a_ads = db.session.query(Ads, Influencer, Campaigns, Sponsor).join(
        Influencer, Ads.influencer_id == Influencer.influencer_id).join(Campaigns, Ads.campaign_id == Campaigns.campaign_id).join(Sponsor, Ads.sponsor_id == Sponsor.sponsor_id).all()
    labels=['Sponsors', 'Influencers', ' Campaigns' ]
    counts=[total_spon, total_usr, total_camp]
  
    colors = ['#ff69b4', '#ffcc00',  '#33cc33']

    
    plt.clf()
    plt.bar(labels, counts, color = colors)
    plt.title('Counts')  
    plt.xlabel('')
    plt.ylabel('Counts')
    for rect, colors in zip(plt.gca().patches, colors):
        rect.set_alpha(0.4)
    plt.savefig('static/bar.png')
    
   
    
    plt.clf()
    if total_aads > 0 or total_rads > 0:
        labels1 = ['Accepted', 'Rejected']
        counts1 = [total_aads, total_rads]
        
        colors1 = ['#FFC300', '#900C3F']
        plt.pie(counts1, labels=labels1, colors=colors1)
        plt.title("ADS")
        for rect, colors in zip(plt.gca().patches, colors1):
            rect.set_alpha(0.6)
        plt.savefig('static/pie.png')
    
    return render_template("admin_dash.html", uname=uname, sponsor=sponsor, influencer=influencer, campaign=campaign,total_rads=total_rads,total_aads=total_aads, ai_ads=ai_ads, a_ads=a_ads, labels = labels, counts = counts)




# @app.route("/remove_ad/<int:ad_id>")
# def remove_ad(ad_id):
#     ads = Ads.query.get(ad_id)
#     db.session.delete(ads)
    
#     db.session.commit()
    
#     return  redirect('/admin_home')




@app.route("/usr_flag/<int:influencer_id>")
def flag_usr(influencer_id):
    influencer = Influencer.query.filter_by(influencer_id = influencer_id).first()
    if influencer.status == 'flagged':
        influencer.status = 'unflagged'
    else:
        influencer.status = 'flagged'
    db.session.commit()
    return redirect(url_for('admin_home'))
    
@app.route("/brand_flag/<int:sponsor_id>")
def flag_brand(sponsor_id):
    sponsor = Sponsor.query.filter_by(sponsor_id = sponsor_id).first()
    if sponsor.status == 'flagged':
        sponsor.status = 'unflagged'
    else:
        sponsor.status = 'flagged'
    db.session.commit()
    return redirect(url_for('admin_home'))
    
@app.route("/ad_flag/<int:ad_id>")
def flag_ads(ad_id):
    ads = Ads.query.filter_by(ad_id = ad_id).first()
    if ads.status == 'flagged':
        ads.status = 'unflagged'
    else:
        ads.status = 'flagged'
    db.session.commit()
    return redirect(url_for('admin_home'))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------Admin-End---------------------------------------------------------------------------------------------           