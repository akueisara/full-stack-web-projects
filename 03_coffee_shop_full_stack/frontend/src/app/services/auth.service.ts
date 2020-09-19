import { Injectable } from '@angular/core';
import { JwtHelperService } from '@auth0/angular-jwt';

import { environment } from '../../environments/environment';

const JWTS_LOCAL_KEY = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1ZjdmMjBhOGNhYzYwMDZmYmJjZTAyIiwiYXVkIjoiY29mZmVlc2hvcCIsImlhdCI6MTYwMDQ5MDQwOCwiZXhwIjoxNjAwNDk3NjA4LCJhenAiOiJlOWtlTzc0aWxQOEZCR0ZHdFlnZVhTNFVta1ZISFhTbyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.C6FngEyaDCnt4I9njz20HfqKJJFEExWC0PBVNNpaiJvG3qmzsVWPandcURPoupaSdFDU0zZ4IO_cWNjtCAQjncQJbMcWgSH_TVX4dozoJGuuGa5KEf2LDeoAl_WuARrL2E6eQ-U6ZYl4JUvHzf2JFJVNSyYpKn5kEtoxmFUifUuhV7RdXl4knTBrdNOLF6Xxir9GuxCnG_5lKhspl848v8bwgX8WuASPgfdgtxQuDiEam0uP_5yuaX4MDqFTZA1mDWluStkUquwUzm0ElOwM4wkLxpZIKEkoAgMugmKvO9_Pf7s0Y1DLaqnQ9cYKlpn9Ud92Cq98MBajn1sEG2a0cA';
const JWTS_ACTIVE_INDEX_KEY = 'JWTS_ACTIVE_INDEX_KEY';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = environment.auth0.url;
  audience = environment.auth0.audience;
  clientId = environment.auth0.clientId;
  callbackURL = environment.auth0.callbackURL;

  token: string;
  payload: any;

  constructor() { }

  build_login_link(callbackPath = '') {
    let link = 'https://';
    link += this.url + '.auth0.com';
    link += '/authorize?';
    link += 'audience=' + this.audience + '&';
    link += 'response_type=token&';
    link += 'client_id=' + this.clientId + '&';
    link += 'redirect_uri=' + this.callbackURL + callbackPath;
    return link;
  }

  // invoked in app.component on load
  check_token_fragment() {
    // parse the fragment
    const fragment = window.location.hash.substr(1).split('&')[0].split('=');
    // check if the fragment includes the access token
    if ( fragment[0] === 'access_token' ) {
      // add the access token to the jwt
      this.token = fragment[1];
      // save jwts to localstore
      this.set_jwt();
    }
  }

  set_jwt() {
    localStorage.setItem(JWTS_LOCAL_KEY, this.token);
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  load_jwts() {
    this.token = localStorage.getItem(JWTS_LOCAL_KEY) || null;
    if (this.token) {
      this.decodeJWT(this.token);
    }
  }

  activeJWT() {
    return this.token;
  }

  decodeJWT(token: string) {
    const jwtservice = new JwtHelperService();
    this.payload = jwtservice.decodeToken(token);
    return this.payload;
  }

  logout() {
    this.token = '';
    this.payload = null;
    this.set_jwt();
  }

  can(permission: string) {
    return this.payload && this.payload.permissions && this.payload.permissions.length && this.payload.permissions.indexOf(permission) >= 0;
  }
}
