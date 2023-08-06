import { c as configureLocalization, s, i, y, u as updateWhenLocaleChanges, a as cleanPath, m as msg, t as tc_filelist, b as tc_fileupload } from './filelist-b70078f3.js';

const supportedLocales = ["en", "zh-CN"];
const {
  getLocale,
  setLocale
} = configureLocalization({
  sourceLocale: "en",
  targetLocales: supportedLocales,
  loadLocale: locale => import(`/static/locale/${locale}.js`)
});
const decideLocale = localeName => {
  if (supppoedLocales.includes(localeName)) {
    return localeName;
  }

  if (localeName.startsWith('en')) {
    return 'en';
  }

  if (localeName.startsWith('zh')) {
    return 'zh-CN';
  }

  return undefined;
};

class tc_settings extends s {
  static properties = {
    content: {}
  };
  static styles = i`pre{margin:0}`;

  constructor() {
    super();
  }

  loadData() {
    fetch("/api/confmgr").then(resp => {
      resp.json().then(res => {
        this.content = res;
      });
    });
  }

  save() {
    var items = this.shadowRoot.querySelectorAll("input"); //.configItem");

    for (var i of items.keys()) {
      var path = items[i].getAttribute("tc-config-tree").split("-");
      var value = items[i].value;
      var orig = this.content;

      for (var n in path.slice(0, -1)) {
        orig = orig[path[n]];
      }

      orig[path.slice(-1)] = value;
    }
  }

  render() {
    if (this.content) {
      var h = [];

      var genHtml = (obj, lavel, name) => {
        if (typeof obj != "object") {
          return y`<input class="configItem" tc-config-tree="${name.slice(1)}" value="${obj}">`;
        }

        var ret = [];

        for (var i in obj) {
          ret.push(y`<pre>${"  ".repeat(lavel)} ${i}:${genHtml(obj[i], lavel + 1, [name, i].join("-"))}<pre></pre></pre>`);
        } //          ret.push(html`<pre>${"   ".repeat(lavel)}<button>New</button><pre>`)


        return ret;
      };

      h = genHtml(this.content, 0, "");
      return y`${h}<button>Summit</button>`;
    }
  }

}
customElements.define("tc-settings", tc_settings);

class tc_shares extends s {
  static properties = {
    shares: {}
  };
  static styles = i`a{color:var(--tc-link-color,#00f);text-decoration:none}`;

  loadData() {
    fetch("/api/shares").then(resp => {
      resp.json().then(res => {
        this.shares = res;
      });
    });
  }

  render() {
    if (!this.shares) {
      return;
    }

    var h = [];

    for (var i in this.shares) {
      var path = this.shares[i].path;

      if (path == "") {
        path = "/";
      }

      h.push(y`<a href="/shares/${i}">${location.origin}/shares/${i}</a> Path: ${path} | User:${this.shares[i].username}<button>del</button><br>`);
    }

    return y`${h}<button>new</button>`;
  }

}
customElements.define("tc-shares", tc_shares);

class tinycloud extends s {
  static properties = {
    url: {},
    routes: {}
  };
  static styles = i`a{color:var(--tc-link-color,#00f)}`;

  constructor() {
    super();
    window.tinycloud = this;
    window.setLocale = setLocale;
    var browserLang = navigator.language;
    setLocale(decideLocale(browserLang) || en);
    updateWhenLocaleChanges(this);

    if (location.hash.split("#")[1]) {
      this.url = cleanPath(location.hash.split("#")[1]);
    } else {
      this.url = "/";
    }

    window.addEventListener("hashchange", () => {
      this.hashchange();
    }, false);
    this.routes = {
      files: [this.contentFiles, msg("Files")],
      settings: [this.contentSettings, msg("Settings")],
      shares: [this.contentShares, msg("Shares")]
    };
  }

  hashchange() {
    this.url = cleanPath(location.hash.split("#")[1]);
  }

  contentSettings = () => {
    var settings = new tc_settings();
    settings.loadData();
    return y`${settings}`;
  };
  contentShares = () => {
    var shares = new tc_shares();
    shares.loadData();
    return y`${shares}`;
  };
  contentFiles = () => {
    var url = "/" + this.url.split("/").slice(2).join("/");
    var urlRoot = this.url.split("/").slice(0, 2).join("/");
    var filelist = new tc_filelist();
    filelist.url = url;
    filelist.urlRoot = urlRoot;
    var fileupload = new tc_fileupload();
    fileupload.url = url;
    fileupload.uploadFinishedCallback = filelist.uploadFinishedCallback;
    fileupload.uploadProgressCallback = filelist.uploadProgressCallback;
    filelist.file_upload = fileupload;
    filelist.loadData();
    return y`${filelist}${fileupload}`;
  }; // Render the UI as a function of component state

  render() {
    //console.log(this.url.split('/')[])
    var menu = [];

    for (var i in this.routes) {
      menu.push([this.routes[i][1], this.routes[i][0], i]);
    }

    if (this.url == "/") {
      location.hash = "/files";
    }

    var contFunc = this.routes[this.url.split("/")[1]][0];
    return y`<body><div id="header">Tinycloud0.1<div align="right">${menu.map(x => y`<a href="#${x[2]}">${msg(x[0])}</a> `)}</div><hr></div><div id="content">${contFunc()}</div></body>`; //Use msg() two times is ugly but work and can let me dont use the callback
  }

}
customElements.define("tc-main", tinycloud);

export { tinycloud };
