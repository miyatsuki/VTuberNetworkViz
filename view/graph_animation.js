Vue.config.devtools = true;
let channel_list;
var channel_image_list; //= ["https://yt3.ggpht.com/a/AGF-l7-NOLCfp1v_PxvXY1WMNGLuMxR59JIpMUnhgQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78hx6ii25kXsCTWBDWaHvlYNPk44NzKdDnIkQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_3F7Uk9fEIwXPZe3h5doe-dNWN9usImrDi=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-YR3ZppjnCTwbgTvuZcPH6pXVfoRUlUXVZ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79eDWXTPZe2Enw2hBvZi-qsB7qiL1UbdUJOkQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78PzRxSDQxi2jCtQxYT4-3GMelm5z6ydptlvw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_OXxl-HOWIQaxDv8KNbYNQOWl6lu0hBflqnw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78NqiqZmVyPMRRySCKTBTzScI39xTeTYXCbYw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-3Dcc3AuL3_FXsiBFgOOBTuL8XUiYIWebhOA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78KCnkQR-3hiGr8RLS5sLU075UDyCwXms3liA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-fHgYkFvGTK5Ts-9YHhADdKaG6krCWL910oA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79L9G_1H0fhygKpcAYW_1InzEwynT7uUTNUNw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78SwKo2lclKWwVhY4YGVY59ajwkLUMZMDBHjA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l794QDYOeL_FbljZU73cJWxKLj8ZJHn7hvfoAQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79lRnEXQg0IPGXkJxx2TyqcjVeVTqwGZdsWwA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78VHYZg2WFMxdxyQkLnb2MQhcvAAZSgb3-uEQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-uPpMX0WRu64RHt2j3xPajkRteDGLuDWFR3A=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-wZHBWAbPf3JhsO_f1drWj0aEt_2R4ngEemw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79T78V0-9yOApYDZHpHN7A5Fke0uJiTcEJWAg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_YXF9WTW_qVXelYeFXTr5jAMP3jqZjSAKi3A=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-HFAksxujKK1d-wpknr9W3aXEFBnzFLjXjmQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-YVWisRIWpad7G2mE5__K3n-24k6hNPZpq2w=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79gkgR05I6pSCM2VQUZfalk4YV0WemNwfXGzg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78MAo5uxC404H_Bz9KaWB55NEEtlHuvcj-VXQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l794vAmgqLTddxhULGtXRw0ucgOECZoacf852g=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-kqCPPlwKw7hMqdrprdBs6eBcLATjbleYUvw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78XVY6iapZNwq26ipDHk4eLu3kBys3nIl8c1w=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78WbCrjx21jKphTRJGoS2ko8fY5OWwFry-Pyw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78nQ16SBsVIzTeummMtgtJRdNddR-v_Qs_rfQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78y7eBRq0GSwxGNZXOaXyAwTLT-BxoK5ohpqw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78jprDdrETIP72ghcoN5BMG73aElVoJaZzvBw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_F1Nm7zCNWWmeQM2gunrs46MdudkohaXv0Bg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79NWtzmM-yOQIFvFNSrui1q_eO7yodDpou5Ag=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-hRtES9KWosuUDU7blqQ-cN_qN1pM1GxPj3w=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-fE2Mhle5lvjeQCxr8ZEtufNkDuCRAg5LSkA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l787rV-sL1M57pmWfcFBDKrIlZvQtA3GoPgubg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78pLdqlQSov5ioYOTeV9gDvSXphNDTEj26Dig=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-Gi7zFBt1gXe9Sl4rNF_osWMVGNZKASCG4hw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-3D5YDtJI5QrNX1YZrmoITlUIRqrLHF0IJaQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78dJU97tROjJS_kUBPEooRb0dndVzhX6Xp_LA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79jh9CH0lngnL5gJuU6C5ePzzXgQ-CDCs7Afg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_ElOeLPWELh-w_O_LNx4MV1O_MM3pH7XNqFg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l797RqHjbIVZqnqiIZRNzRdoctiw1PPh10A7LA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-ZI26nfpyT5RpePovfIqJ7uoqhPFTiLC0OMQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78O3ZBZy7Z6Xvunp0VRixWSPFEP9pMUhkBODQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78YnmyE3snkHMp_18AZOP5QRH2WOYSBlnPKFA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-c1NWuEQRgBfgryqZmRH-9g7RITGgnQouaNQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79zbc_ymqkoY-GBKHyFDG8mtQwWk7p_CYW-Hg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_rPWdBeEN4wNmK9g52VRvDm1BSXGlSiaEwPw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79Vb9rz5ACtGW1YTCpnj5XFlqpwT6q1-SD7=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_XeICb6sZ0keumRyeoLyUTOJydQQCgfEBrYw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l797yMpOSt808Cx6bS4B1V7oz_HvB30hIe02iA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-ICBzdKCrBbqi_Py88NMhSs9vYWl90D2wrZA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78QUJmKPULTDMBRlUdaWtzLL9BTLye1WtxAog=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-qUv-puWNfCl4p5PeXflEYeTO79ZrAdX3Q=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-UNyEmD0j83USGZgfmop0lR5u1e_bVc087vw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l797jz-6GjNrInag0IYDdFBSG8K-OGJ4kPIYEQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79gadShrMVOeZevaBkL5IKmyx_7sRfxl_kjkQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_AQCRUteV-qi7_TTquMFXOi4wf_CotKkpDRQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78UdWk_9gZGnCkMgHr_O_R1M1raW5gSvXMH_w=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_pnHKx_lioPtmWeHGMW_yRsoKXg8CUQ-OdBA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79CTnTrMPJupy09_b8EeDmYN5F76pcqe2Ryew=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79p_R2nrPonwGV1-55uhWWw6GUO8Y3WD0SELw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-vJk9vwuWozWErKkcbyJntlVUyq7O5QSR8Eg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_rmtymgg66IzyXcNx4NcBctFs_s6OtFV4YCg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-OQI7tY9x5HmzP4nLXKyjsgjCatrfwnLWsDg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79HPXfTNfu61MIr_igZ3Tv9hk5Nb94j1OT3MQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79FqXiIjgQn-IaS6lTkIjONltnsG52yvV42tg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79FVhOlqpIAgv94IbSVMRFw7inrg6WF1DPcrQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-_h5zNb12kC6RvqaIeU4D76RSvNkZiys12VQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78Dn33A7SSQksXgT6zB0_k2f2ysEz0-_ZOthw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-zIf7VFqw2EDC3l7y_UpaxfdrAu-YEQcRGJA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l78JwRlRIlR82frAXYbjZ_a6yHSj8njkMMBQvA=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-2cdwsQelHighTZd2Y5YPokTByjA5sMmOSgQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l780SqNJnUtUmRCu8Cg4PIdEBzO9b1VIJ0XDcQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_rTF5ICrnh3rObRriyQAREWpv2e6WusYFHdg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l79eOdM-7T5y9OCTQirBBF7AKR5WWxs46HBcPg=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7-20CGdX9MeEm0ZE3zmj4t9f4J9MtSpYFBRfQ=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_wQhhnzM2X_sJmjT1cYnyj1zMQIHfTnycBqw=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_aTKh2iRgHQekI6BumUQvIDZ3VVDYRrAOUag=s240-c-k-c0xffffffff-no-rj-mo", "https://yt3.ggpht.com/a/AGF-l7_XJI0pHpYCWDzv4l0-9U4p8g8WXypKecghTA=s240-c-k-c0xffffffff-no-rj-mo"]

let collab_mat_map;
let subscriber_map;

svg_size = 6400

getConfig = async() => {
  var promise1 = await fetch("/data.json", {
    method : "GET"
  })
  var json = await promise1.json()
  collab_mat_map = json["collab_mat_list"]
  subscriber_map = json["subscriber_map"]
  channel_list = json["channel_list"]
  channel_info = json["channels"]
  console.log(json)
}

unixtime = 1567868400

async function init(){
  await getConfig()
  const app = new Vue({
    el: '#app',
    data: {
      channel_list : channel_list,
      channel_image_list : channel_image_list,
      positions: setInitialPosition(channel_list),
      collab_times_mat: collab_mat_map[unixtime],
      collab_subscriber_list: subscriber_map[unixtime],
      unixtime : unixtime
    },
    methods: {
      getImageUrl : function(index){
        channel_id = channel_list[index]
        return channel_info[channel_id]["image_url"]
      },
      getClipDefName: function(index){
        return "clipPath_" + index
      },
      getClipUsageName: function(index){
        return "clip-path: url(#clipPath_" + index + ");"
      },
      getLineWidth: function(from_index, to_index){
        sum = 0
        collab_array = collab_mat_map[unixtime][from_index]
        for(var i = 0; i < collab_array.length; i++){
          sum += collab_array[i]  
        }
        return collab_mat_map[unixtime][from_index][to_index]/sum
      },
      getCircleSize: function(index){
        return Math.pow(subscriber_map[unixtime][index], 0.35)
      },
      unixtimeToYYYYMMDD: function(unixtime){
        d = new Date(unixtime * 1000)
        yyyy = d.getFullYear()
        mm = ('0' + (d.getMonth() + 1)).slice(-2)
        dd = ('0' + (d.getDate() + 1)).slice(-2)
        return yyyy + "-" + mm + "-" + dd + "(" + unixtime + ")"
      }
    }
})

setInterval(function(){
  if (collab_mat_map[unixtime + 24 * 3600]){
    unixtime += 24 * 3600
  }
  app.unixtime = unixtime
  console.log(app.unixtime)
  app.collab_times_mat = collab_mat_map[unixtime]
  app.collab_subscriber_list = subscriber_map[unixtime]
}, 1000)

setInterval(function(){
  updatePosition(app.positions, collab_mat_map[unixtime])
}, 20)

}
onload = function() {
    init()
};

function setInitialPosition(channel_list){
  ans = []
  for(var i = 0; i < channel_list.length; i++){
    ans.push({"posX" : Math.random()*svg_size, "posY": Math.random()* svg_size})
  }
  return ans;
}

function getDistanceBetweenNodes(i, j){
  size_i =  10 + Math.pow(subscriber_map[unixtime][i], 0.35)
  size_j =  10 + Math.pow(subscriber_map[unixtime][j], 0.35)
  return size_i + size_j
}

const coulomb = 2000000
const bounce = 20
const attenuation = 0.9

function updatePosition(positions, collab_times_mat){
  updateOnThisMove = false
  for(var i = 0; i < collab_times_mat.length; i++){
    force = [0, 0]
    if(subscriber_map[unixtime][i] == 0){
      continue
    }

    channel_subscribers = subscriber_map[unixtime][i];
    for(var j = 0; j < collab_times_mat.length; j++){
      if(i == j || subscriber_map[unixtime][j] == 0){
        continue
      }

      distanceX = positions[i]["posX"] - positions[j]["posX"]
      distanceY = positions[i]["posY"] - positions[j]["posY"]
      distance = Math.sqrt(Math.pow(distanceX, 2) + Math.pow(distanceY, 2)) + Number.EPSILON

      force[0] += coulomb * distanceX/Math.pow(distance, 2) 
      force[1] += coulomb * distanceY/Math.pow(distance, 2)
    }

    for(var j = 0; j < collab_times_mat.length; j++){
      if(i == j){
        continue
      }

      distanceX = (positions[j]["posX"] - positions[i]["posX"])
      distanceY = (positions[j]["posY"] - positions[i]["posY"])

      force[0] += bounce * (distanceX - (getDistanceBetweenNodes(i, j) + 10)) * collab_times_mat[i][j]
      force[1] += bounce * (distanceY - (getDistanceBetweenNodes(i, j) + 10)) * collab_times_mat[i][j]
    }

    //本当は前のループの値を保持しておく必要がある
    velocity = [0, 0]
    velocity[0] = (velocity[0] + force[0]) * attenuation / (channel_subscribers + 1)
    velocity[1] = (velocity[1] + force[1]) * attenuation / (channel_subscribers + 1)

    if(Math.abs(velocity[0]) + Math.abs(velocity[1]) < 5){
      continue
    }

    
    posX = positions[i]["posX"] + velocity[0]
    if(posX < 0){
      posX = 0
    }
    else if(posX > svg_size){
      posX = svg_size
    }
    positions[i]["posX"] = posX

    posY = positions[i]["posY"] + velocity[1]
    if(posY < 0){
      posY = 0
    }
    else if(posY > svg_size){
      posY = svg_size
    }

    positions[i]["posY"] = posY 
  }
}
