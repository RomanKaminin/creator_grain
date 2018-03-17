<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8"%>

<%@page import="ru.curs.showcase.security.SecurityParamsFactory"%>   
<%@page import="ru.curs.showcase.runtime.UserDataUtils"%> 
<%@page import="ru.curs.showcase.security.esia.EsiaSettings"%>
<%@page import="ru.curs.showcase.runtime.AppInfoSingleton"%>
<%@page import="ru.curs.showcase.app.server.AppAndSessionEventsListener"%>
<%@page import="org.springframework.security.web.savedrequest.DefaultSavedRequest"%>
<%@page import="org.springframework.security.web.savedrequest.HttpSessionRequestCache"%>

<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>

<html>
<head>

<%
	String title = "Авторизация в КУРС: Showcase";
	if (UserDataUtils.getGeneralOptionalProp("login.title") != null) {
		title = UserDataUtils.getGeneralOptionalProp("login.title");
	}

	String webAppName = request.getContextPath();
	if (webAppName.contains("/")) {
		webAppName = webAppName.replace("/", "");
	}
	
	if(request.getParameter("error") == null && request.getParameter("exited") == null)
	{
		Cookie cookie = new Cookie("queryString" + request.getServerPort() + webAppName, "");
		cookie.setPath(AppAndSessionEventsListener.getContextPath());
		response.addCookie(cookie);
	}
	if(request.getParameter("exited") != null)
	{
		Cookie[] cookies = request.getCookies();
		if (cookies != null && cookies.length > 0) {
			for (Cookie cookie : cookies) {
				if (cookie.getName().equals("queryString" + request.getServerPort() + webAppName)
						&& cookie.getValue() != null && cookie.getValue().contains("autologin=true")) {
					Cookie removeAutologinCookie = new Cookie("queryString" + request.getServerPort() + webAppName, "");
					removeAutologinCookie.setPath(AppAndSessionEventsListener.getContextPath());
					response.addCookie(removeAutologinCookie);
				}
			}
		}
	}
%>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

	<title><%=title%></title>
	<link rel="shortcut icon" href="solutions/default/resources/favicon.ico" type="image/x-icon" />
	<link rel="icon" href="solutions/default/resources/favicon.ico" type="image/x-icon" />
	
    <script type="text/javascript">
    	var djConfig = {
            parseOnLoad: false,
            isDebug: false
        };
    </script>  
	<script src="js/dojo/dojo.js"></script>
	
<script type="text/javascript">

	function checkAuthenticationImageSize() {
		<%DefaultSavedRequest defaultSavedRequest =
			(DefaultSavedRequest) (new HttpSessionRequestCache().getRequest(request, response)); 
	
		String autologin = "false";
		
	if(defaultSavedRequest != null)
	{
		if(defaultSavedRequest.getQueryString() != null &&
				defaultSavedRequest.getQueryString().contains("autologin=true")){
				 autologin = "true";
		}}%>
		
		dojo.xhrGet({
			sync: true,
			url: "<%=request.getContextPath()%>/auth/isAutologinServlet?autologin=<%=autologin%>",
			handleAs: 'json',
			preventCache: true,
			timeout: 10000,
			load: function(data) {
				document.getElementsByName('j_username')[0].value = data.login;
				document.getElementsByName('j_password')[0].value = data.pwd;
				if(data.submit === "true"){
					document.formlogin.submit();
					return;
				}
			},
			error: function(error) {
				alert("Ошибка автологина.");
			}
		});
		
		var w;
		<%if (UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication") != null && "true".equalsIgnoreCase(UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication").trim())) {%>
		var pic = document.getElementById("authenticationImage");
		w = pic.naturalWidth;<%}%>  
		<%if (UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication") == null || !("true".equalsIgnoreCase(UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication").trim()))) {%>
		w = 1000;
		<%}%>
		
		if (w == 178) {	
			if (document.getElementById('helloMessage')) 
		 		dojo.attr("helloMessage", "innerHTML", "");
			if (document.getElementById('informationMessage')) 
				dojo.attr("informationMessage", "innerHTML", "Идет проверка подлинности пользователя...<br>Пожалуйста подождите...");
			id = setTimeout("checkIsAuthenticatedSession()",1000);
		}
		else {			
			<%if (!autologin.equals("true")) { %>
		    document.formlogin.style.display = "";
		    document.getElementById("j_username").focus();
			<%}%>
			
		}
	}
	
	function checkIsAuthenticatedSession() {
		dojo.xhrGet({
			sync: true,
			url: "<%=request.getContextPath()%>/auth/isAuthenticatedServlet?sesid=<%=request.getSession().getId()%>",
			handleAs: "json",
			preventCache: true,
			timeout: 10000,
			load: function(data) {
				document.getElementsByName("j_username")[0].value = data.login;
				document.getElementsByName("j_password")[0].value = data.pwd;
				document.formlogin.submit();
			},
			error: function(error) {
				alert("Ошибка соединения с сервером аутентификации.");
			}
		});
	}
   
</script>	
	
	
	
</head>
<body onLoad="checkAuthenticationImageSize()">

     <!--[if lte IE 7]>
     <p style="margin: 0.2em 0; background: #ccc; color: #000; padding: 0.2em 0;">Ваша текущая версия Internet explorer устарела. Приложение будет работать некорректно. <a href="http://browsehappy.com/">Обновите свой браузер!</a></p>
     <![endif]-->

<%  
	if(UserDataUtils.getGeneralOptionalProp("security.ssl.keystore.path") != null){
		System.setProperty("javax.net.ssl.trustStore", 
				UserDataUtils.getGeneralOptionalProp("security.ssl.keystore.path").trim());
	}

String authGifSrc = String.format("%s/authentication.gif?sesid=%s",
		SecurityParamsFactory.getAuthServerUrl(), request.getSession() 
				.getId());

authGifSrc = SecurityParamsFactory.correctAuthGifSrcRequestInCaseOfInaccessibility(authGifSrc);
%>
<c:if test="${not empty param.error}">
<div id="accessDenied">
  <font color="red">
  <b>Ошибка!</b>
  <br/>
  <%if(((Exception)request.getSession().
		  getAttribute("SPRING_SECURITY_LAST_EXCEPTION")).getMessage().contains("Bad credentials")) {%>
  Имя пользователя и/или пароль неверны!<br/>
  Отказано в доступе. <br/>
  <%}%>
  Ответ сервера: ${sessionScope["SPRING_SECURITY_LAST_EXCEPTION"].message} 
  <br/>
  </font>
  </div>
</c:if>

<form class="formlogin" name="formlogin" method="POST" action="<c:url value="/j_spring_security_check" />">

    
<table>
	<img src="http://localhost:8080/example/resources/login_content/logokurs.png" height="103" weight="153" style="margin: 0px 12px 10px 0px;"><br>
    <span id="helloMessage">Авторизация в КУРС</span>
    <span id="informationMessage" style="font-family: sans-serif;"></span>

    <p>
        <%--<label for="j_username" style="width: 150px;display: inline-block;padding: 3px;">Имя пользователя</label>--%>
        <input id="j_username" type="text" name="j_username" placeholder="Введите имя пользователя" />
    </p>
    <p>
        <%--<label for="j_password" style="width: 150px;display: inline-block;padding: 3px;">Пароль</label>--%>
        <input  id="j_password" type="password" name="j_password" autocomplete = "off" placeholder="Введите пароль" />
    </p>
    <p>
        <label for="remember_me">Запомнить меня</label>
        <input type="checkbox" name="_spring_security_remember_me" id="remember_me" />
    </p>

    <div style="text-align: center;">
        </p>
            <input class="submit" type="submit" value="Войти" />
            <input class="submit" type="reset" value="Сбросить" />
        </p>
    </div>

    <td><%if (UserDataUtils.getGeneralOauth2Properties() != null) {%><a href="oauth?auth=websphere">WebSphere авторизация</a><%}%> <%if (UserDataUtils.getGeneralSpnegoProperties() != null) {%><a href="spnego">Spnego авторизация</a><%}%></td>

</table>
</form>

<br/>
<%if (UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication") != null && "true".equalsIgnoreCase(UserDataUtils.getGeneralOptionalProp("security.crossdomain.authentication").trim())) {%><img src="<%=authGifSrc%>" alt=" " id="authenticationImage" style="visibility:hidden" /><%}%>

     <style>
         .formlogin{
             width: 370px;
             margin: auto;
             text-align: center;
             height: 275px;
             position: absolute;
             left: 50%;
             top: 50%;
             margin-left: -200px;
             margin-top: -200px;
         }
         #helloMessage{
             font-size: 27px;
             color:#481b92;
         }
         #j_username, #j_password{
             height: 30px;
             width: 233px;
             padding: 6px 8px;
         }
         .submit {
             background-color: #3c1b72;;
             background: linear-gradient(top, #c504a2, #920290);
             border: 1px solid #bac0c3;
             border-bottom: 1px solid #999;
             color: white;
             font-weight: bold;
             padding: 6px 0px;
             text-align: center;
             text-shadow: 0 -1px 0 #000;
             width: 135px;
         }
         .submit:hover {
             opacity:.85;
             cursor: pointer;
         }
         .submit:active {
         }

     </style>
</body>
</html>
