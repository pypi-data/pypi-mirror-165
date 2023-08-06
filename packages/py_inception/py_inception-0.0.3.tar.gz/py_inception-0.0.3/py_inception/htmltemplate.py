from . import __version__

HEAD = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>Inception</title>"""

BODY = f"""<link rel="icon" href="data:image/svg+xml;utf8, %3Csvg xmlns='http://www.w3.org/2000/svg' width='32' height='32'%3E%3Cpath style='fill:%23000000;stroke:%23000000;stroke-width:0.172538;stroke-linecap:square;stroke-linejoin:bevel;stroke-dashoffset:5;paint-order:markers stroke fill' d='m 13.177938,0.08716153 c -0.484932,-0.008491 -1.028351,0.03608697 -1.09612,0.89727855 -0.212741,2.85001692 -0.348602,6.58568572 -0.70657,9.61810592 -0.537789,4.55563 0.08265,7.421638 -11.11721364,9.323727 -0.28416718,0.09089 -0.17168286,1.178717 0.0215814,1.313004 5.46144844,2.820784 8.20579594,0.449207 11.80000824,9.747571 0.44161,0.89141 0.990791,0.756204 1.301046,0.769223 V 0.09176527 c -0.06532,-0.0013267 -0.133455,-0.0035379 -0.202732,-0.0047762 z m 0.409361,0 c -0.06928,0.0013267 -0.1374,0.0035379 -0.202733,0.0047762 V 31.756244 c 0.250778,-0.02711 0.425132,0.134313 0.866742,-0.757097 3.210214,-8.757166 8.12889,-7.372908 12.233959,-9.759698 0.193265,-0.134287 0.305749,-1.22211 0.02158,-1.313008 C 15.306985,18.024357 15.927428,15.158349 15.389635,10.602714 15.031671,7.5702983 14.89581,3.8346295 14.683065,0.98461255 14.615287,0.12339002 14.072235,0.07882969 13.587303,0.08733843 Z' /%3E%3Cpath style='fill:%23ffffff;fill-rule:evenodd;stroke:%23ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1' d='m 17.160731,22.162537 c 3.099415,-0.160844 6.106251,-0.38196 9.204034,-1.944163 -2.954832,-0.462997 -5.485192,-0.808459 -9.197984,-3.343414 1.393528,1.462451 2.695237,3.020705 4.483925,3.597575 -3.019917,0.997995 -3.060612,0.791034 -4.395131,1.107361 z' /%3E%3Cpath style='fill:%23ffffff;fill-rule:evenodd;stroke:%23ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1' d='M 12.397013,22.589734 C 8.6210076,22.083491 3.5162806,22.219299 0.48910593,20.0872 L 2.8053895,19.705483 C 4.89,20.745947 6.3404219,21.621157 12.397013,22.589734 Z' /%3E%3Cpath style='mix-blend-mode:normal;fill:%23ffffff;fill-rule:evenodd;stroke:%23ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1' d='M 13.428724,0.55226327 C 12.954579,0.70836152 12.677819,1.0903881 12.57839,1.4752361 c 0.430094,0.4582028 0.248111,2.697492 0.397407,0.9791244 L 12.033782,15.016902 c -0.264948,1.197459 -1.373163,2.609835 -2.5742212,3.390008 1.3921732,0.701038 3.2120492,0.917299 4.8847332,0.629408 -0.729916,-1.44611 -0.9537,-2.937011 -1.043484,-4.439759 L 13.558447,2.0947689 c 0.061,-0.3401506 0.123364,-0.6804339 0.479837,-1.0498698 -0.334706,-0.33917335 -0.491813,-0.44207869 -0.60956,-0.49263583 z' /%3E%3C/svg%3E" />
<body>
<div id="main-container">
    <div id="main-sidebar">
        <div id="sidebar-header">
            <svg width="27" height="32">
                <path style="fill:#000000;stroke:#000000;stroke-width:0.172538;stroke-linecap:square;stroke-linejoin:bevel;stroke-dashoffset:5;paint-order:markers stroke fill" d="m 13.177938,0.08716153 c -0.484932,-0.008491 -1.028351,0.03608697 -1.09612,0.89727855 -0.212741,2.85001692 -0.348602,6.58568572 -0.70657,9.61810592 -0.537789,4.55563 0.08265,7.421638 -11.11721364,9.323727 -0.28416718,0.09089 -0.17168286,1.178717 0.0215814,1.313004 5.46144844,2.820784 8.20579594,0.449207 11.80000824,9.747571 0.44161,0.89141 0.990791,0.756204 1.301046,0.769223 V 0.09176527 c -0.06532,-0.0013267 -0.133455,-0.0035379 -0.202732,-0.0047762 z m 0.409361,0 c -0.06928,0.0013267 -0.1374,0.0035379 -0.202733,0.0047762 V 31.756244 c 0.250778,-0.02711 0.425132,0.134313 0.866742,-0.757097 3.210214,-8.757166 8.12889,-7.372908 12.233959,-9.759698 0.193265,-0.134287 0.305749,-1.22211 0.02158,-1.313008 C 15.306985,18.024357 15.927428,15.158349 15.389635,10.602714 15.031671,7.5702983 14.89581,3.8346295 14.683065,0.98461255 14.615287,0.12339002 14.072235,0.07882969 13.587303,0.08733843 Z" />
                <path style="fill:#ffffff;fill-rule:evenodd;stroke:#ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" d="m 17.160731,22.162537 c 3.099415,-0.160844 6.106251,-0.38196 9.204034,-1.944163 -2.954832,-0.462997 -5.485192,-0.808459 -9.197984,-3.343414 1.393528,1.462451 2.695237,3.020705 4.483925,3.597575 -3.019917,0.997995 -3.060612,0.791034 -4.395131,1.107361 z" />
                <path style="fill:#ffffff;fill-rule:evenodd;stroke:#ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" d="M 12.397013,22.589734 C 8.6210076,22.083491 3.5162806,22.219299 0.48910593,20.0872 L 2.8053895,19.705483 C 4.89,20.745947 6.3404219,21.621157 12.397013,22.589734 Z" />
                <path style="mix-blend-mode:normal;fill:#ffffff;fill-rule:evenodd;stroke:#ffffff;stroke-width:0.181153px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" d="M 13.428724,0.55226327 C 12.954579,0.70836152 12.677819,1.0903881 12.57839,1.4752361 c 0.430094,0.4582028 0.248111,2.697492 0.397407,0.9791244 L 12.033782,15.016902 c -0.264948,1.197459 -1.373163,2.609835 -2.5742212,3.390008 1.3921732,0.701038 3.2120492,0.917299 4.8847332,0.629408 -0.729916,-1.44611 -0.9537,-2.937011 -1.043484,-4.439759 L 13.558447,2.0947689 c 0.061,-0.3401506 0.123364,-0.6804339 0.479837,-1.0498698 -0.334706,-0.33917335 -0.491813,-0.44207869 -0.60956,-0.49263583 z" />
            </svg>
            <div> <span class="title">Inception</span><br> <span class="ver">{__version__}</span> </div>
        </div>
        <div id="sidebar-menu">
            <div onclick="$UI.set_tab('objects', 'sb')" id="tab-sb-objects">🗐</div>
            <div onclick="$UI.set_tab('props', 'sb')" id="tab-sb-props">🖹</div>
        </div>
        <div id="sidebar-content">
            <div id="panel-sb-objects">
                <div id="sb-objects-lst" class="scroll6"></div>
            </div>
            <div id="panel-sb-props">
                <div id="sb-props-lst" class="scroll6"></div>
            </div>
        </div>
    </div>
    <div id="main-switch">
        <div onclick="$UI.toggle_sidebar()" id="tb-sbt">❮</div>
        <a href="#" onclick="$UI.set_tab('mro', 'main')" id="tab-main-mro">MRO</a>
        <a href="#" onclick="$UI.set_tab('tree', 'main')" id="tab-main-tree">Tree</a>
        <a href="#" onclick="$UI.set_tab('object', 'main')" id="tab-main-object">Object</a>
    </div>
    <div id="main-content"> 
        <div id="panel-main-mro"> 
            <div id="out_object" class="out"></div>
            <div id="out_class" class="out"></div>
            <div id="out_metaclass" class="out"></div>
        </div>
        <div id="panel-main-tree"> 
            <div class="tree-svg-menu">
                <div class="tb-btn tb-toggle" id="act_svg_reverse">Reverse</div>
                <div class="optgroup tb-toggle">
                    <div class="tb-btn" id="act_svg_compact">Compact</div>
                    <div class="tb-btn active" id="act_svg_module">Module</div>
                    <div class="tb-btn" id="act_svg_metaclass">Metaclass</div>
                </div>
            </div>
            <svg id="out_tree"></svg>
        </div>
        <div id="panel-main-object"> 
        </div>
    </div>
</div>
"""

SCRIPT = """
<script>
    const $Cfg = {
        render: {
            str_trim: 30,
            svg_compact: {
                w: 180,
                h: 22,
                x_space: 10,
                y_space: 10,
                x_pad: 20,
                y_pad: 32,
            },
            svg_info: {
                w: 200,
                h: 42,
                x_space: 32,
                y_space: 32,
                x_pad: 20,
                y_pad: 32,
            },
            svg_mode: "module",
            svg_reverse: 0,
        },
        tab: {
            sb: undefined,
            main: undefined,
        },
        cur_inspect: undefined,
        cur_select: undefined,
    };
    const $DOM = {
        id: (id) => document.getElementById(id),
        cls: (cls) => document.getElementsByClassName(cls),
        sb: document.getElementById("main-sidebar"),
        sb_toggle: document.getElementById("tb-sbt"),
        sb_props_lst: document.getElementById("sb-props-lst"),
        sb_objects_lst: document.getElementById("sb-objects-lst"),
        main_mro_obj: document.getElementById("out_object"),
        main_mro_cls: document.getElementById("out_class"),
        main_mro_mcls: document.getElementById("out_metaclass"),
        main_tree_svg: document.getElementById("out_tree"),
        main_object: document.getElementById("panel-main-object"),
    }
    const $I = {
        // Interface for Inception data model
        all: () => model.objects,
        dict: (id) => model.dicts[id].items,
        dictType: (id) => model.dicts[id].type,
        list: (id) => model.lists[id].items,
        listType: (id) => model.lists[id].type,
        func: (id) => model.funcs[id],
        obj: (id) => model.objects[id],
        objClass: (id) => $I.obj(id).class,
        objClassName: (id) => $I.obj($I.obj(id).class).name,
        objName: (id) => $I.obj(id).name === undefined ? "id: " + id : $I.obj(id).name,
        objModule: (id) => $I.obj(id).module == undefined ? "---" : $I.obj(id).module,
        objCategory(id) {
            if ($I.obj(id)) return "obj";
            if ($I.isList(id)) return "list";
            if ($I.isDict(id)) return "dict";
            if ($I.isFunc(id)) return "func";
            if ($I.isString(id)) return "string";
            return undefined;
        },
        string: (id) => model.strings[id],
        idObject: () => model.object,
        idType: () => model.type,
        target: () => model.targets,
        isClass: (id) => (($I.obj(id) != undefined) && ($I.obj(id).mro != undefined)),
        isDict: (id) => (model.dicts[id] != undefined),
        isList: (id) => (model.lists[id] != undefined),
        isFunc: (id) => (model.funcs[id] != undefined),
        isString: (id) => (model.strings[id] != undefined),
        sortByName(a, b) {
            if ($I.objName(a) < $I.objName(b)) return -1;
            if ($I.objName(a) > $I.objName(b)) return 1;
            return 0;
        },
    }
    const $UI = {
        by_id: {
            act_svg_reverse: (set) => {$Cfg.render.svg_reverse=set; $Render.tree();},
            act_svg_compact: () => {$Cfg.render.svg_mode="compact"; $Render.tree();},
            act_svg_module: () => {$Cfg.render.svg_mode="module"; $Render.tree();},
            act_svg_metaclass: () => {$Cfg.render.svg_mode="metaclass"; $Render.tree();},
        },
        set_inspect(){
            $Cfg.cur_inspect = $Cfg.cur_select;
            $Render.mro();
            $Render.tree();
            $Render.main_object();
            $UI.hl_inspect();
        },
        set_select(obj){
            $Cfg.cur_select = obj;
            $Render.sb_props();
            $UI.hl_select();
        },
        set_tab(tab, group){
            if ($Cfg.tab[group]!=undefined) {
                $DOM.id("tab-" + group + "-" + $Cfg.tab[group]).classList.remove("active");
                $DOM.id("panel-" + group + "-" + $Cfg.tab[group]).classList.remove("active");
            }
            $Cfg.tab[group] = tab;
            $DOM.id("tab-" + group + "-" + tab).classList.add("active");
            $DOM.id("panel-" + group + "-" + tab).classList.add("active");
        },
        toggle_fold(tgt){
            if (tgt.classList.contains("act_fold")) {
                tgt.classList.remove("act_fold");
                tgt.classList.add("act_unfold");
                tgt.innerHTML = "▶";
                tgt.parentNode.nextElementSibling.style.display = "none";
            } else if (tgt.classList.contains("act_unfold")) {
                tgt.classList.remove("act_unfold");
                tgt.classList.add("act_fold");
                tgt.innerHTML = "▼";
                tgt.parentNode.nextElementSibling.style.display = "";
            }
        },
        toggle_sidebar(){
            $DOM.sb_toggle.innerHTML = ($DOM.sb.style.display == "none") ? "❮" : "❯";
            $DOM.sb.style.display = ($DOM.sb.style.display == "none") ? "" : "none";
        },
        click_list(tgt){
            // Click on list item event
            // If item is "object" - select it, else try to fold/unfold
            if (tgt.classList.contains("objitem")){
                for(const i of tgt.classList) if (i.startsWith("o_")) return $UI.set_select(i.slice(2));
            } else $UI.toggle_fold(tgt);
        },
        click_tb_btn(tgt){
            var set = 1;
            // Click on toolbar button
            if (tgt.classList.contains("tb-toggle")){
                if (tgt.classList.contains("active")){
                    tgt.classList.remove("active");
                    set = 0;
                } else tgt.classList.add("active");
            } else if (tgt.parentNode.classList.contains("tb-toggle")){
                const l = tgt.parentNode.getElementsByClassName("active");
                while (l.length>0) l[0].classList.remove("active");
                tgt.classList.add("active");
            }
            if ($UI.by_id[tgt.id]!=undefined) $UI.by_id[tgt.id](set);
        },
        hl_inspect(){
            const c = $DOM.cls("objinspect");
            while(c.length > 0) c[0].classList.remove("objinspect");
            for(const i of $DOM.cls("o_" + $Cfg.cur_inspect)) i.classList.add("objinspect");
        },
        hl_select(){
            const c = $DOM.cls("objselect");
            while(c.length > 0) c[0].classList.remove("objselect");
            const l = $DOM.cls("lens");
            while(l.length > 0) l[0].remove();

            for(const i of $DOM.cls("o_"+$Cfg.cur_select)) {
                if (i.classList.contains("objitem")) {
                    $Tpl.span({cls:"lens", html: "🔍", append_to: i.parentNode}).onclick = $UI.set_inspect;
                    i.classList.add("objselect");
                } else {
                    $Tpl.span({cls: "lens", html: "🔍", append_to: i.parentNode}).onclick = $UI.set_inspect;
                    i.parentNode.parentNode.classList.add("objselect");
                }
            }
        },
        init(){
            $DOM.sb_objects_lst.addEventListener("click", (evt) => $UI.click_list(evt.target));
            $DOM.sb_props_lst.addEventListener("click", (evt) => $UI.click_list(evt.target));
            for(const i of $DOM.cls("tb-btn")) i.addEventListener("click", (evt) => $UI.click_tb_btn(evt.target));
            $UI.hl_inspect();
            $UI.set_tab("mro", "main");
            $UI.set_tab("objects", "sb");
        },
    }
    const $Tpl = {
        // Template and tools for HTML element and block
        escape(text) {
            return text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#039;');
        },
        element(type, {cls, html, id, append_to, display}={}) {
            const e = document.createElement(type);
            if (cls) for (const c of [].concat(cls)) e.classList.add(c);
            if (id) e.id = id;
            if (display) e.style.display = display;
            if (html != undefined) for (const c of [].concat(html)) e.append(c);
            if (append_to) append_to.appendChild(e);
            return e;
        },
        update(elem, {add_cls, display, onclick}) {
            if (add_cls) for (const c of [].concat(add_cls)) elem.classList.add(c);
            if (display) elem.style.display = display;
            if (onclick) elem.onclick = onclick;
            return elem;
        },
        p: (param) => $Tpl.element("p", param),
        span: (param) => $Tpl.element("span", param),
        div: (param) => $Tpl.element("div", param),
        badge: (val) => $Tpl.element("span", {cls: "badge", html: val}),
        sign: (val) => $Tpl.element("span", {cls: "sign", html: val}),
        trprop(name, val, append_to){
            const tr = $Tpl.element("tr", {append_to: append_to,});
            $Tpl.element("td", {html: name, append_to: tr} );
            $Tpl.element("td", {html: val, append_to: tr} );
            return tr;
        },
        objitem(id, badge) {
            const e = $Tpl.span({cls: ["objitem", "o_" + id], html: $I.objName(id)});
            if (badge > 0) e.append($Tpl.badge(badge));
            return e;
        },
        lstIcon: {
            fold: () => $Tpl.span({cls: ["act", "act_fold", "icon_sm"], html: "▼"}),
            unfold: () => $Tpl.span({cls: ["act", "act_unfold", "icon_sm"], html: "▶"}),
            dot: () => $Tpl.span({cls: "icon_sm", html: "・"}),
        },
        lstLine(icon, nodes = []) {
            return $Tpl.div({cls: "_lst_line", html: [$Tpl.lstIcon[icon]()].concat(nodes) });
        },
        svgElement(type, attr = {}, {append_to}){
            const e = document.createElementNS('http://www.w3.org/2000/svg',type);
            for(const a in attr) e.setAttribute(a, attr[a]);
            if (append_to != undefined) append_to.appendChild(e);
            return e;
        },
        svgLine(x1, y1, w, h, {stroke, append_to}){
            const s = (stroke == undefined) ? "black" : stroke;
            const line = $Tpl.svgElement("line", {x1, y1, "x2": x1 + w, "y2": y1 + h, "stroke": s}, {append_to});
            return line
        },
        svgFO(x, y, width, height, elem, append_to){
            const FO = $Tpl.svgElement("foreignObject", {x, y, width, height}, {append_to});
            FO.append(elem);
            return FO;
        },
    }
    const $Render = {
        // Render pages and blocks
        prop_line_gen: {
            default(blk){
                if ($I.isClass(blk.id)) return $Tpl.span({html: $I.objName(blk.id) })
                return $Tpl.span({html: $I.objClassName(blk.id)+"()" })
            },
            dict: (blk) => $Tpl.span({html: [blk.type + " ", $Tpl.badge(blk.len)] }),
            dir:  (blk) => $Tpl.span({html: blk.val}),
            func: (blk) => $Tpl.span({html: [$Tpl.sign("ƒ "), blk.type, "()"] }),
            list: (blk) => $Tpl.span({html: [blk.type, $Tpl.badge(blk.len)] }),
            str(blk) {
                const s = $I.string(blk.id);
                if (s.length < $Cfg.render.str_trim) return $Tpl.span({html: '"' + $Tpl.escape(s) + '"'});
                return $Tpl.span({html: '"' + $Tpl.escape(s.substring(0, $Cfg.render.str_trim-2)) + '…"'});
            },
        },
        prop_block_gen: {
            default: (blk) => undefined,
            str(blk) {
                const s = $I.string(blk.id);
                if (s.length < $Cfg.render.str_trim) return undefined;
                return $Tpl.div({html: '"' + $Tpl.escape(s) + '"'});
            },
            list(blk) {
                if (blk.len == 0) return undefined;
                const block = $Tpl.div();
                for(const i of $I.list(blk.id)) block.appendChild($Tpl.lstLine("dot", $Render.prop_line(i)));
                return block;
            },
            dict(blk) {
                if (blk.len == 0) return undefined;
                const block = $Tpl.div();
                for(const i of $I.dict(blk.id))
                    block.appendChild($Tpl.lstLine("dot", [$Render.prop_line(i[0]), ": ", $Render.prop_line(i[1])] ));
                return block;
            },
        },
        object_card_gen: {
            default: (id) => undefined,
            obj(id, {level}){
                const obj = $I.obj(id);
                var header = $Tpl.div({cls: "blk-head", html: $Tpl.div({html: "Object: " + $I.objName(id) }) });
                var content = $Tpl.div({cls: "content" });
                var card = $Tpl.div({cls:["full-card"], html: [header, content]});

                // attributes
                if (obj.dict != undefined){
                    var attributes = $Tpl.div({cls: ["panel", "attributes"], html: "Object: " + id});
                    const tbl = $Tpl.element("table", {append_to: content});
                    for(const e of Object.keys(obj.dict).sort()){
                        const tr = $Tpl.element("tr", {
                            html: [
                                $Tpl.element("td", {html: e}),
                                $Tpl.element("td", {html: $Render.prop_line(obj.dict[e]) }),
                            ],
                            append_to: tbl,
                        });
                        if (obj.dict[e].id!=undefined) $Tpl.update(tr, {
                            add_cls: "act",
                            onclick: () => $Render.main_object_card(obj.dict[e].id, level+1),
                        });
                    }
                }
                return card;
            },
            func(id, {level}){
                const obj = $I.func(id);
                var header = $Tpl.div({cls: "blk-head", html: $Tpl.div({html: "Callable: " + obj.name }) });
                var content = $Tpl.div({cls: "content" });
                var card = $Tpl.div({cls:["full-card"], html: [header, content]});

                const tbl = $Tpl.element("table", {append_to: content});
                $Tpl.trprop("Module", obj.module, tbl);
                $Tpl.trprop("Name", obj.name, tbl);
                $Tpl.trprop("Qualname", obj.qualname, tbl);
                
                if (obj.doc){
                    const tr = $Tpl.trprop("Doc", $Render.prop_line(obj.doc), tbl);
                    if (obj.doc.id) $Tpl.update(tr, 
                        {add_cls: "act", onclick: () => $Render.main_object_card(obj.doc.id, level+1),});
                }

                if (obj.co_filename) {
                    $Tpl.element("br", {append_to: content});
                    $Tpl.p({html: ["File: ", obj.co_filename, ":", obj.co_firstlineno], append_to: content});
                }

                if (obj.pos_args==undefined) return card
                
                $Tpl.element("br", {append_to: content});
                $Tpl.p({html: "Arguments:", append_to: content});
                const tbl2 = $Tpl.element("table", {append_to: content});
                function farg(p, append_to) {
                    const tr = $Tpl.element("tr", {append_to});
                    $Tpl.element("td", {html: p.name, append_to: tr} );
                    $Tpl.element("td", {html: p.def ? p.def : " ", append_to: tr} );
                    $Tpl.element("td", {html: p.ann ? p.ann : " ", append_to: tr} );
                    return tr;
                }
                const tr = $Tpl.element("tr", {append_to: tbl2});
                $Tpl.element("th", {html: "Name", append_to: tr} );
                $Tpl.element("th", {html: "Default", append_to: tr} );
                $Tpl.element("th", {html: "Annotation", append_to: tr} );
                
                if (obj.posonlyargcount>0) 
                    $Tpl.element("td", {html: "Position only args", cls: "center", append_to:
                        $Tpl.element("tr", {append_to: tbl2})
                    } ).colSpan = 3;
                
                for(const i in obj.pos_args) {
                    if (obj.posonlyargcount == i)
                        $Tpl.element("td", {html: "Position/KW args", cls: "center", append_to: 
                            $Tpl.element("tr", {append_to: tbl2})
                        } ).colSpan = 3;
                    const p = obj.pos_args[i];
                    farg(p, tbl2);
                }

                if (obj.kw_args.length > 0)
                    $Tpl.element("td", {html: "KW only args", cls: "center", 
                        append_to: $Tpl.element("tr", {append_to: tbl2})
                    } ).colSpan = 3;
                for(const i in obj.kw_args) {
                    const p = obj.kw_args[i];
                    farg(p, tbl2);
                }

                return card;
            },
            string(id, {level}) {
                const str = $I.string(id);
                var header = $Tpl.div({cls: "blk-head", html: $Tpl.div({html: "String: " + id }) });
                var content = $Tpl.div({cls: "content", html: $Tpl.element("pre", {html: $Tpl.escape(str) }) });
                var card = $Tpl.div({cls:["full-card"], html: [header, content]});
                return card;
            },
            dict(id, {level}) {
                const dict = $I.dict(id);
                var header = $Tpl.div({cls: "blk-head", html: $Tpl.div({html: "Dict: " + id }) });
                var content = $Tpl.div({cls: "content"});
                var card = $Tpl.div({cls:["full-card"], html: [header, content]});

                var attributes = $Tpl.div({cls: ["panel", "attributes"], html: "Object: " + id});
                const tbl = $Tpl.element("table", {append_to: content});
                for(const e of dict){
                    const tr = $Tpl.element("tr", {append_to: tbl});
                    const td1 = $Tpl.element("td", {html: $Render.prop_line(e[0]), append_to: tr} );
                    const td2 = $Tpl.element("td", {html: $Render.prop_line(e[1]), append_to: tr} );

                    if (e[0].id!=undefined) $Tpl.update(td1, {
                        add_cls: "act",
                        onclick: () => $Render.main_object_card(e[0].id, level+1),
                    });
                    if (e[1].id!=undefined) $Tpl.update(td2, {
                        add_cls: "act",
                        onclick: () => $Render.main_object_card(e[1].id, level+1),
                    });

                }
                return card;
            },
            list(id, {level}) {
                const lst = $I.list(id);
                var header = $Tpl.div({cls: "blk-head", html: $Tpl.div({html: "List: " + id }) });
                var content = $Tpl.div({cls: "content"});
                var card = $Tpl.div({cls:["full-card"], html: [header, content]});

                var attributes = $Tpl.div({cls: ["panel", "attributes"], html: "Object: " + id});
                const tbl = $Tpl.element("table", {append_to: content});
                for(const e of lst){
                    const tr = $Tpl.element("tr", {
                        html: $Tpl.element("td", {html: [$Render.prop_line(e)]} ),
                        append_to: tbl,
                    });
                    if (e.id!=undefined){
                        tr.classList.add("act");
                        tr.onclick = function(evt){ $Render.main_object_card(e.id, level+1); };
                    }
                }
                return card;
            },
        },
        prop_line(blk, param) {
            const handler = $Render.prop_line_gen[blk.mode];
            return handler!=undefined ? handler(blk, param) : $Render.prop_line_gen.default(blk, param);
        },
        prop_block(blk, param) {
            const handler = $Render.prop_block_gen[blk.mode];
            return handler!=undefined ? handler(blk, param) : $Render.prop_block_gen.default(blk, param);
        },
        object_card(id, param) {
            const handler = $Render.object_card_gen[$I.objCategory(id)];
            return handler!=undefined ? handler(id, param) : $Render.object_card_gen.default(id, param);
        },
        mro_block(id){
            // Render object block for main/MRO 
            const obj = $I.obj(id);
            const header = $Tpl.div({cls: "blk-head", html: [
                $Tpl.div({html:  $Tpl.span({cls: ["o_" + id], html: $I.objName(id) }) }),
                $Tpl.div({cls: "module", html: "🖿 " + $I.objModule(id) }),
            ]});

            header.onclick = () => $UI.set_select(id);
            const content = $Tpl.div({cls: ["content", "scroll6"]});

            if ( (obj.class!==undefined) && ($I.obj(obj.class).name!="type") )
                content.append( $Tpl.p({html: "type: " + $I.obj(obj.class).name}) );
            if (obj.bases!==undefined) {
                content.append( $Tpl.p({html: "bases:"}) );
                for(const i of obj.bases) content.append( $Tpl.p({cls: "lmarg", html: $I.obj(i).name}) );
            }
            if (obj.dict!==undefined) {
                content.append( $Tpl.p({html: "dict:"}) );
                for(const i in obj.dict) content.append( $Tpl.p({cls: "lmarg", html: i }) );
            }
            return $Tpl.div({cls: "block", html: [header, content]});
        },
        mro(id){
            // Render main/MRO. Rerender on inspect changes.
            if (id == undefined) id = $Cfg.cur_inspect;
            $DOM.main_mro_obj.innerHTML="";
            $DOM.main_mro_cls.innerHTML="";
            $DOM.main_mro_mcls.innerHTML="";
            const cls = $I.isClass(id) ? id : $I.obj(id).class;
            const metacls = $I.obj(cls).class;

            if (! $I.isClass(id)) 
                $DOM.main_mro_obj.appendChild($Render.mro_block(id));
            for(const i of $I.obj(cls).mro)
                $DOM.main_mro_cls.appendChild($Render.mro_block(i));
            for(const i of $I.obj(metacls).mro)
                if (i != $I.idObject()) $DOM.main_mro_mcls.appendChild($Render.mro_block(i));
        },
        tree_branch(branch, off_x, off_y){
            // Render main/tree branch on svg canvas.
            const svg = $Cfg.render[$Cfg.render.svg_mode=="compact" ? "svg_compact" : "svg_info"];
            const half_ydist = (svg.h + svg.y_space) / 2;
            const half_xspace = svg.x_space / 2;

            // Render object block
            var block_y = off_y + (branch.count - 1) * half_ydist;
            const div = $Tpl.div({cls:"blk-head", html:
                $Tpl.div({html: $Tpl.span({cls:"o_" + branch.obj, html: $I.objName(branch.obj) }) }), });
            if ($Cfg.render.svg_mode=="module")
                $Tpl.div({cls: "module", html: "🖿 " + $I.objModule(branch.obj), append_to: div });
            if ($Cfg.render.svg_mode=="metaclass")
                $Tpl.div({cls: "module", html: "⟁ " + $I.objClassName(branch.obj), append_to: div });
            div.onclick = () => $UI.set_select(branch.obj);
            $Tpl.svgFO(off_x, block_y, svg.w, svg.h, div, $DOM.main_tree_svg);

            if (branch.children.length == 0) return;

            // Draw link line from current block to children
            $Tpl.svgLine(off_x + svg.w, block_y + svg.h / 2, half_xspace, 0, {append_to: $DOM.main_tree_svg});
            // Vertical-part of link line
            if (branch.children.length > 1) {
                const vert_y = off_y + (branch.children[0].count - 1) * half_ydist + svg.h / 2;
                const vert_h = half_ydist * (branch.count * 2 - branch.children[branch.children.length-1].count - branch.children[0].count);
                $Tpl.svgLine(off_x + svg.w + half_xspace, vert_y, 0, vert_h, {append_to: $DOM.main_tree_svg});
            }
            
            // Recursive render children branch
            var child_y = off_y;
            for(const c of branch.children){
                // Render branch
                const cbl = $Render.tree_branch(c, off_x + svg.w + svg.x_space, child_y);
                // Render link line from vertical-part to branch
                const vy = child_y + (c.count - 1) * half_ydist + svg.h / 2;
                $Tpl.svgLine(off_x + svg.w + half_xspace, vy, half_xspace, 0, {append_to: $DOM.main_tree_svg});
                child_y += c.count * (svg.h + svg.y_space);
            }
        },
        tree(id){
            // Render main/tree (class hierarhy). Rerender on inspect changes.
            const svg = $Cfg.render[$Cfg.render.svg_mode=="compact" ? "svg_compact" : "svg_info"];
            if (id == undefined) id = $Cfg.cur_inspect;
            if ($I.obj(id).bases == undefined) id = $I.obj(id).class;

            // Formating tree struture (nodes may duplicate)
            function make_tree(obj){
                var res = {obj, children: [], depth: 1, count: 0};
                var lst = [];
                if ($Cfg.render.svg_reverse=="0") lst = $I.obj(obj).bases;
                else for(const i in $I.all()) 
                    if ($I.obj(i).bases && $I.obj(i).bases.includes(parseInt(obj))) lst.push(i);
                for(const c of lst){
                    if (c == $I.idObject()) continue;
                    const branch = make_tree(c);
                    res.children.push(branch);
                    res.count += branch.count;
                    if (branch.depth >= res.depth) res.depth = branch.depth + 1;
                }
                if (res.count==0) res.count = 1;
                return res;
            }
            var tree = make_tree(id);

            // Set size of svg canvas and render tree
            $DOM.main_tree_svg.style.width = svg.w * tree.depth + svg.x_space * (tree.depth - 1) + svg.x_pad * 2 + "px";
            $DOM.main_tree_svg.style.height = svg.h * tree.count + svg.y_space * (tree.count - 1) + svg.y_pad * 2 + "px";
            $DOM.main_tree_svg.innerHTML = "";
            $Render.tree_branch(tree, svg.x_pad, svg.y_pad)
        },
        sb_objects(){
            // Render sidebar/objects list. Renders once, doesn't change.
            var modules = {};
            var classes = {};

            // Prepare tree data
            for(const id in $I.all()) {
                if ($I.isClass(id)) {
                    if (modules[$I.objModule(id)]==undefined) modules[$I.objModule(id)] = [];
                    if (classes[id]==undefined) classes[id] = [];
                    modules[$I.objModule(id)].push(id);
                } else {
                    if (classes[$I.objClass(id)]==undefined) classes[$I.objClass(id)] = [];
                    classes[$I.objClass(id)].push(id)
                }
            }
            
            // Rendering tree
            for(const name of Object.keys(modules).sort()){
                // Add folder for module
                const el = $Tpl.lstLine("fold", [name, $Tpl.badge(modules[name].length)]);
                $DOM.sb_objects_lst.appendChild(el);

                // Adds folders or lines (if there are no instances) for module classes
                const mod_blk = $Tpl.div({cls: "_lst_bl", append_to: $DOM.sb_objects_lst});
                for(const clsid of modules[name].sort($I.sortByName)){
                    const obj_count = classes[clsid].length;
                    const el = $Tpl.lstLine( (obj_count==0) ? "dot" : "unfold", $Tpl.objitem(clsid, obj_count));
                    mod_blk.append(el);
                    
                    // Add instances
                    if (obj_count > 0) {
                        const blk = $Tpl.div({cls: "_lst_bl", append_to: mod_blk, display: "none"});
                        for(const id of classes[clsid].sort()) blk.append( $Tpl.lstLine("dot", $Tpl.objitem(id)) );
                    }
                }
            }
        },
        sb_props(id){
            // Render sidebar/props list. Rerenders on selection changes.
            if (id==undefined) id = $Cfg.cur_select;
            const obj = $I.obj(id);
            $DOM.sb_props_lst.innerHTML = '';

            // Main object info: id, name, class, module
            $DOM.sb_props_lst.appendChild($Tpl.lstLine("fold", "id: " + id));
            const info = $Tpl.div({cls: "_lst_bl", append_to: $DOM.sb_props_lst});
            if (obj.name)   info.append( $Tpl.lstLine("dot", "Name: " + obj.name) );
            if (obj.class)  info.append( $Tpl.lstLine("dot", "Class: " + $I.obj(obj.class).name) );
            if (obj.module) info.append( $Tpl.lstLine("dot", "Module: " + obj.module) );
            
            if (obj.dict){
                const content = [];
                const content_f = [];
                $DOM.sb_props_lst.appendChild($Tpl.lstLine("fold", "__dict__"));
                for(const d of Object.keys(obj.dict).sort()){
                    const prop = obj.dict[d];
                    const el = $Render.prop_line(prop);
                    const blk = $Render.prop_block(prop);
                    const ico = blk ? "unfold" : "dot";
                    const target = prop.mode == "func" ? content_f : content;
                    target.push($Tpl.lstLine(ico, [$Tpl.span({cls: "propname", html: d}), ": ", el]));
                    if (blk) target.push($Tpl.update(blk, {add_cls: ["_lst_bl", "_lst_val"], display: "none"}))
                }
                $Tpl.div({cls: "_lst_bl", html: content_f.concat(content), append_to: $DOM.sb_props_lst});
            }
        },
        main_object(){
            // Render main/object
            $DOM.main_object.innerHTML = "";
            $Render.main_object_card($Cfg.cur_select, 1);
        },
        main_object_card(id, level){
            // Clean main/object panels >= level
            const panels = $DOM.main_object.children;
            while(panels.length >= level) panels[level-1].remove();
            // Add new panel with card
            var card = $Render.object_card(id, {level});
            if (!card) return;
            $Tpl.div({cls:["column", "level-" + level], html: card, append_to: $DOM.main_object});
            $DOM.main_object.scrollLeft = $DOM.main_object.scrollWidth - $DOM.main_object.clientWidth;
        },
        init(){
            $Render.sb_objects();
            $Render.mro();
            $Render.tree();
            $Render.sb_props();
            $Render.main_object();
        },
    }

    $Cfg.cur_inspect = $I.target()[0];
    $Cfg.cur_select = $I.target()[0];
    $Render.init();
    $UI.init();
</script>
"""

CSS = """<style>
/* Variables */

:root {
    --c-back: #cad3d9;
    --c-backwhite: #fff;
    --c-border: #a5acb1;
    --c-divider: #73777a;
    --c-active: #69b5e5;
    --c-shadow: #3b3d3f;
    --c-bagebg: #a8cbe0;
    --c-bagefg: #000520;
    --c-inspect: #69b5e5;
    --c-inspectbg: #69b5e552;
    --c-valuebg: #69b5e532;
    --c-selectbg: #ffd96f;
    --c-cardbg: #f3fff5;
    --c-carddivbg:#9dccb7;
    --c-cardheaderbg: #aee3cb;
    --w-sidebar: 300px;
    --w-objectblock: 400px;
  }

/* Tag reset */

body {
    position: absolute;
    top: 0px;
    bottom: 0px;
    left: 0px;
    right: 0px;
    padding: 0px;
    margin: 0px;
    overflow: hidden;
    font-family: sans-serif;
}

p {
    padding: 0px;
    margin: 0px;
}

/* Common elements */

.blk-head {
    padding: 0px;
    background-color: var(--c-cardheaderbg);
    border-bottom: 1px solid var(--c-divider);
    cursor: pointer;
}
.blk-head > div {
    padding: 2px 4px;
    margin: 0px;
    border-top: 1px solid var(--c-carddivbg); 
}
.blk-head > div:first-child { border-top-width: 0px; }
.blk-head.objselect { background-color: var(--c-selectbg); }
.blk-head .lens {
    float: right;
    width: 12px;
    margin-left: -12px;
}
#panel-main-tree .blk-head{
    width: 100%;
    height: 100%;
    font-size: 80%;
    border: 1px solid var(--c-divider);
    box-sizing: border-box;
    cursor: pointer;
}

.lmarg { margin-left: 14px; }
.act { cursor: pointer; }
.bold {font-weight: bold;}
.center {text-align: center;}
.lens {
    display: inline-block;
    cursor: pointer;
    height: 14px;
    margin: -2px 2px;
    border-radius: 4px;
}
.lens:hover { background-color: var(--c-active); }

.propname { font-weight: bold; }

.objinspect {
    border: 1px dashed var(--c-inspect);
    background-color: var(--c-inspectbg);
}

.objitem { cursor: pointer; }
.objitem.objselect { background-color: var(--c-selectbg); }

.badge {
    background-color: var(--c-bagebg);
    color: var(--c-bagefg);
    padding: 1px 6px;
    font-size: 80%;
    border-radius: 4px;
    margin-left: 4px;
}

.icon_sm {
    display: inline-block;
    padding-left: 2px;
    padding-right: 6px;
    font-size: 10px;
    width: 10px;
    text-align: center;
    color: var(--c-active);
}

.sign {
    display: inline-block;
    font-size: 110%;
    font-weight: bold;
    color: var(--c-active);
}

._lst_line { padding: 1px 4px 0px 4px; }
._lst_bl {
    margin-left: 11px;
    border-left: 1px solid var(--c-active);
    margin-bottom: 6px;
    padding-top: 1px;
}
._lst_val {
    padding: 1px 5px;
    margin-right: 10px;
    background-color: var(--c-valuebg);
    overflow-wrap: break-word;
}

.scroll6::-webkit-scrollbar {
    height: 6px;
    width: 6px;
}
.scroll6::-webkit-scrollbar-track {
    background-color: #ffff;
    border-radius: 10px;
    margin: 6px;
}
.scroll6::-webkit-scrollbar-thumb {
    background-color: var(--c-border);
    border-radius: 10px;
}
.scroll6::-webkit-scrollbar-corner {
    background-color: #ffff;
}

/* Main: Layout */

#main-container {
    display: flex;
    overflow: hidden;
    width: 100%;
    height: 100%;
    flex-flow: row nowrap;
    align-content: stretch;
}

#main-content {
    flex-grow: 1;
    overflow: auto;
}

#main-content > div { display: none; }
#sidebar-content > div { display: none; }

/* Main: Sidebar */

#main-sidebar {
    display: flex;
    flex-flow: column nowrap;
    width: var(--w-sidebar);
    min-width: var(--w-sidebar);
    max-width: var(--w-sidebar);
    height: 100%;
    background-color: var(--c-back);
    border-right: 1px solid var(--c-divider);
    box-shadow: 1px 0px 3px var(--c-divider);
    z-index: 30;
}

#sidebar-header { padding: 10px 20px; }
#sidebar-header .ver { font-size: 60%; }
#sidebar-header > div{
    display: inline-block;
    height: 100%;
    text-align: left;
    padding-left: 10px;
}

#sidebar-menu {
    display: flex;
    flex-flow: row wrap;
    justify-content: left;
    font-size: 20px;
    border-bottom: 1px solid var(--c-border);
    padding-left: 8px;
}
#sidebar-menu div{
    padding-top: 3px;
    height: 29px;
    width: 32px;
    border: 1px solid var(--c-border);
    border-bottom-width: 0px;
    text-align: center;
    cursor: pointer;
    margin-right: -1px;
}
#sidebar-menu .active { background-color: var(--c-active); }

#sidebar-content {
    flex-shrink: 1;
    overflow: hidden;
    height: 100%;
}

#panel-sb-objects.active {
    display: flex;
    flex-flow: column nowrap;
    height: 100%;
}

#sb-objects-lst {
    flex-shrink: 1;
    flex-grow: 1;
    overflow: auto;
    margin: 10px;
    border: 1px solid var(--c-border);
    background-color: var(--c-backwhite);
    font-size: 80%;
    max-height: 100%;
}

#sb-props-lst {
    flex-shrink: 1;
    flex-grow: 1;
    overflow: auto;
    margin: 10px;
    border: 1px solid var(--c-border);
    background-color: var(--c-backwhite);
    font-size: 80%;
    max-height: 100%;
}

#panel-sb-props.active {
    display: flex;
    flex-flow: column nowrap;
    height: 100%;
}

/*  Main: Mode switch  */

#main-switch {
    background-color: var(--c-back);
    border-right: 1px solid var(--c-divider);
    box-shadow: 1px 0px 6px var(--c-shadow);
    width: 26px;
    font-size: 90%;
    z-index: 20;
}
#main-switch a{
    display: block;
    width: 18px;
    padding: 16px 4px;
    text-decoration: none;
    color: #222;
    border-top: 1px solid var(--c-divider);
    writing-mode: vertical-lr;
    transform: rotate(-180deg);
    -webkit-transform: rotate(-180deg);
    -moz-transform: rotate(-180deg);
}
#main-switch div{
    display: block;
    color: #222;
    width: 18px;
    padding: 16px 4px;
    border-bottom: 1px solid var(--c-divider);
    cursor: pointer;
    text-align: center;
}
#main-switch .active{
    background-color: var(--c-active);
    width: 20px;
    border-left: 1px solid var(--c-divider);
    box-shadow: -3px 0px 6px var(--c-divider);
}

/* MRO View CSS */

#panel-main-mro.active {
    display: flex;
    flex-flow: column wrap;
    height: 100%;
    flex-grow: 1;
    min-height: 840px;
}

.out {
    padding-left: 14px;
    display: flex;
    flex-flow: row nowrap;
    min-height: 280px;
    flex-basis: content;
    border-bottom: 1px solid var(--c-border);
}

#out_object { background: rgb(207 226 233); }
#out_class { background: rgb(239 221 207); }
#out_metaclass {
    background: rgb(240 249 248);
    flex-grow: 1;
}

.block {
    display: flex;
    flex-direction: column;
    width: 200px;
    height: 240px;
    margin: 20px;
    background-color: var(--c-cardbg);
    border: 1px solid var(--c-divider);
    font-size: 80%;
}

.block .content {
    padding: 4px;
    overflow: auto;
    height: 100%;
}

/* Tree View CSS */

#panel-main-tree.active {
    display: block;
    height: 100%;
    width: 100%;
}

.tree-svg-menu {
    position: fixed;
    top: 0px;
    padding: 3px 10px;
    font-size: 80%;
}

.tree-svg-menu .optgroup {
    float: left;
    margin: 0px 10px;
}

.tree-svg-menu .optgroup .tb-btn {
    margin: 0px;
    border-left-width: 0px;
    border-radius: 0px;
}

.tree-svg-menu .optgroup :first-child{
    border-left-width: 1px;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
}
.tree-svg-menu .optgroup :last-child{
    border-bottom-right-radius: 4px;
    border-top-right-radius: 4px;
}

.tree-svg-menu .tb-btn {
    float: left;
    margin: 0px 10px;
    padding: 2px 5px;
    background-color: var(--c-back);
    border-radius: 4px;
    border: 1px solid var(--c-border);
    cursor: pointer;
}

.tree-svg-menu .tb-btn.active {
    background-color: var(--c-active);
}

/* Object View CSS */

#panel-main-object.active {
    display: flex;
    flex-flow: row nowrap;
    height: 100%;
    width: 100%;
    overflow-y: hidden;
    overflow-x: auto;
    padding-left: 5px;
    box-sizing: border-box;
}

#panel-main-object .column {
    height: 100%;
    width: var(--w-objectblock);
    min-width: var(--w-objectblock);
    max-width: var(--w-objectblock);
    padding: 10px 5px;
    border-right: 1px dashed var(--c-back);
    overflow-y: auto;
    overflow-x: hidden;
    font-size: 80%;
}

.full-card {
    box-sizing: border-box;
    width: 100%;
    min-height: 60px;
    background-color: var(--c-cardbg);
    border: 1px solid var(--c-divider);
    overflow-x: auto;
}

.full-card .content { padding: 10px; }
.full-card .content pre { 
    padding: 2px;
    background-color: var(--c-backwhite);
    overflow: auto;
}

.full-card table {
    width: 100%;
    min-width: 100%;
    max-width: 100%;
    background-color: var(--c-backwhite);
    border: 1px solid var(--c-border);
    border-collapse: collapse; 
    overflow: auto;
}
.full-card table th{ 
    background-color: var(--c-cardheaderbg); 
    font-weight: normal;
}
.full-card table tr{ border-bottom: 1px solid var(--c-back); }
.full-card table tr:hover{ background-color: var(--c-back); }
.full-card table tr.act:hover{ background-color: var(--c-bagebg); }
.full-card table td { 
    padding: 1px 8px; 
    border-right: 1px solid var(--c-back);
    word-wrap: break-word;
    word-break: break-all;
}
</style>
"""
