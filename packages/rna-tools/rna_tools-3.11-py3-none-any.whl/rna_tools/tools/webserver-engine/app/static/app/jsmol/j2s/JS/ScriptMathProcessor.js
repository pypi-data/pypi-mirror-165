Clazz.declarePackage ("JS");
Clazz.load (null, "JS.ScriptMathProcessor", ["java.lang.Float", "java.util.Arrays", "$.Hashtable", "JU.A4", "$.AU", "$.BS", "$.CU", "$.DF", "$.Lst", "$.M3", "$.M4", "$.P3", "$.P4", "$.PT", "$.Quat", "$.V3", "JM.BondSet", "JS.SV", "$.T", "JU.BSUtil", "$.Escape", "$.Logger"], function () {
c$ = Clazz.decorateAsClass (function () {
this.wasX = false;
this.asBitSet = false;
this.oPt = -1;
this.chk = false;
this.wasSyntaxCheck = false;
this.debugHigh = false;
this.eval = null;
this.vwr = null;
this.oStack = null;
this.xStack = null;
this.ifStack = null;
this.ifPt = -1;
this.xPt = -1;
this.parenCount = 0;
this.squareCount = 0;
this.braceCount = 0;
this.isArrayItem = false;
this.asVector = false;
this.haveSpaceBeforeSquare = false;
this.equalCount = 0;
this.ptid = 0;
this.ptx = 2147483647;
this.pto = 2147483647;
this.isSpecialAssignment = false;
this.doSelections = true;
this.assignLeft = false;
this.allowUnderflow = false;
this.isAssignment = false;
this.skipping = false;
this.lastAssignedString = null;
Clazz.instantialize (this, arguments);
}, JS, "ScriptMathProcessor");
Clazz.prepareFields (c$, function () {
this.oStack =  new Array (8);
this.xStack =  new Array (8);
this.ifStack =  Clazz.newCharArray (8, '\0');
});
Clazz.makeConstructor (c$, 
function (eval, isSpecialAssignment, isArrayItem, asVector, asBitSet, allowUnderflow, key) {
this.eval = eval;
this.isSpecialAssignment = this.assignLeft = isSpecialAssignment;
this.isAssignment = (isSpecialAssignment || key != null);
this.vwr = eval.vwr;
this.debugHigh = eval.debugHigh;
this.chk = this.wasSyntaxCheck = eval.chk;
this.isArrayItem = isArrayItem;
this.asVector = asVector || isArrayItem;
this.asBitSet = asBitSet;
this.allowUnderflow = allowUnderflow;
this.wasX = isArrayItem;
if (this.debugHigh) JU.Logger.debug ("initialize RPN");
}, "JS.ScriptExpr,~B,~B,~B,~B,~B,~S");
Clazz.defineMethod (c$, "endAssignment", 
function () {
this.assignLeft = false;
return (this.doSelections = false);
});
Clazz.defineMethod (c$, "getResult", 
function () {
var isOK = true;
while (isOK && this.oPt >= 0 && this.oStack[this.oPt] != null) isOK = this.operate ();

if (isOK) {
if (this.asVector) {
if (this.isAssignment && (this.xPt > 0 && this.oPt < 0 || this.oPt >= 0 && (this.oStack[this.oPt] != null))) this.eval.invArg ();
var result =  new JU.Lst ();
for (var i = 0; i <= this.xPt; i++) result.addLast (this.isSpecialAssignment ? this.xStack[i] : JS.SV.selectItemVar (this.xStack[i]));

if (this.lastAssignedString != null) {
result.remove (0);
result.add (0, this.lastAssignedString);
this.lastAssignedString.intValue = this.xStack[0].intValue;
}return JS.SV.newV (135198, result);
}if (this.xPt == 0) {
var x = this.xStack[0];
if (this.chk) {
if (this.asBitSet) return JS.SV.newV (10,  new JU.BS ());
return x;
}if (x.tok == 10 || x.tok == 7 || x.tok == 15 || x.tok == 4 || x.tok == 11 || x.tok == 12) x = JS.SV.selectItemVar (x);
if (this.asBitSet && x.tok == 7) x = JS.SV.newV (10, JS.SV.unEscapeBitSetArray (x.value, false));
return x;
}}if (!this.allowUnderflow && (this.xPt >= 0 || this.oPt >= 0)) this.eval.invArg ();
return null;
});
Clazz.defineMethod (c$, "putX", 
 function (x) {
if (this.skipping) return;
if (this.wasX) {
try {
this.addOp (JS.T.tokenComma);
} catch (e) {
if (Clazz.exceptionOf (e, JS.ScriptException)) {
System.out.println ("Error adding comma");
} else {
throw e;
}
}
}if (++this.xPt == this.xStack.length) this.xStack = JU.AU.doubleLength (this.xStack);
this.xStack[this.xPt] = x;
this.ptx = ++this.ptid;
if (this.debugHigh) {
JU.Logger.debug ("\nputx= " + x + " ptx=" + this.ptid);
}}, "JS.SV");
Clazz.defineMethod (c$, "putOp", 
 function (op) {
if (++this.oPt >= this.oStack.length) this.oStack = JU.AU.doubleLength (this.oStack);
this.oStack[this.oPt] = op;
this.pto = ++this.ptid;
if (this.debugHigh) {
JU.Logger.debug ("\nputop=" + op + " pto=" + this.ptid);
}}, "JS.T");
Clazz.defineMethod (c$, "putIf", 
 function (c) {
if (++this.ifPt >= this.ifStack.length) this.ifStack = JU.AU.doubleLength (this.ifStack);
this.ifStack[this.ifPt] = c;
}, "~S");
Clazz.defineMethod (c$, "addXCopy", 
function (x) {
switch (x.tok) {
case 2:
x = JS.SV.newI (x.intValue);
break;
case 3:
x = JS.SV.newV (3, x.value);
break;
}
return this.addX (x);
}, "JS.SV");
Clazz.defineMethod (c$, "addX", 
function (x) {
this.putX (x);
return this.wasX = true;
}, "JS.SV");
Clazz.defineMethod (c$, "addXObj", 
function (x) {
var v = JS.SV.getVariable (x);
if (v == null) return false;
this.putX (v);
return this.wasX = true;
}, "~O");
Clazz.defineMethod (c$, "addXStr", 
function (x) {
this.putX (JS.SV.newS (x));
return this.wasX = true;
}, "~S");
Clazz.defineMethod (c$, "addXBool", 
function (x) {
this.putX (JS.SV.getBoolean (x));
return this.wasX = true;
}, "~B");
Clazz.defineMethod (c$, "addXInt", 
function (x) {
this.putX (JS.SV.newI (x));
return this.wasX = true;
}, "~N");
Clazz.defineMethod (c$, "addXList", 
function (x) {
this.putX (JS.SV.getVariableList (x));
return this.wasX = true;
}, "JU.Lst");
Clazz.defineMethod (c$, "addXMap", 
function (x) {
this.putX (JS.SV.getVariableMap (x));
return this.wasX = true;
}, "java.util.Map");
Clazz.defineMethod (c$, "addXM3", 
function (x) {
this.putX (JS.SV.newV (11, x));
return this.wasX = true;
}, "JU.M3");
Clazz.defineMethod (c$, "addXM4", 
function (x) {
this.putX (JS.SV.newV (12, x));
return this.wasX = true;
}, "JU.M4");
Clazz.defineMethod (c$, "addXFloat", 
function (x) {
if (Float.isNaN (x)) return this.addXStr ("NaN");
this.putX (JS.SV.newV (3, Float.$valueOf (x)));
return this.wasX = true;
}, "~N");
Clazz.defineMethod (c$, "addXBs", 
function (bs) {
this.putX (JS.SV.newV (10, bs));
return this.wasX = true;
}, "JU.BS");
Clazz.defineMethod (c$, "addXPt", 
function (pt) {
this.putX (JS.SV.newV (8, pt));
return this.wasX = true;
}, "JU.P3");
Clazz.defineMethod (c$, "addXPt4", 
function (pt) {
this.putX (JS.SV.newV (9, pt));
return this.wasX = true;
}, "JU.P4");
Clazz.defineMethod (c$, "addXNum", 
function (x) {
var v;
if (Clazz.instanceOf (x, JS.SV)) {
v = x;
} else {
switch (x.tok) {
case 3:
if (this.wasX) {
var f = (x.value).floatValue ();
if (f < 0 || f == 0 && 1 / f == -Infinity) {
this.addOp (JS.T.tokenMinus);
v = JS.SV.newV (3, Float.$valueOf (-f));
break;
}}v = JS.SV.newV (3, x.value);
break;
default:
var iv = x.intValue;
if (this.wasX && iv < 0) {
this.addOp (JS.T.tokenMinus);
iv = -iv;
}v = JS.SV.newI (iv);
break;
}
}this.putX (v);
return this.wasX = true;
}, "JS.T");
Clazz.defineMethod (c$, "addXAV", 
function (x) {
this.putX (JS.SV.getVariableAV (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAD", 
function (x) {
this.putX (JS.SV.getVariableAD (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAS", 
function (x) {
this.putX (JS.SV.getVariableAS (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAI", 
function (x) {
this.putX (JS.SV.getVariableAI (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAII", 
function (x) {
this.putX (JS.SV.getVariableAII (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAF", 
function (x) {
this.putX (JS.SV.getVariableAF (x));
return this.wasX = true;
}, "~A");
Clazz.defineMethod (c$, "addXAFF", 
function (x) {
this.putX (JS.SV.getVariableAFF (x));
return this.wasX = true;
}, "~A");
c$.isOpFunc = Clazz.defineMethod (c$, "isOpFunc", 
 function (op) {
return (JS.T.tokAttr (op.tok, 135266304) && op !== JS.T.tokenArraySquare || op.tok == 269484241 && JS.T.tokAttr (op.intValue, 135266304));
}, "JS.T");
Clazz.defineMethod (c$, "addOp", 
function (op) {
return this.addOpAllowMath (op, true);
}, "JS.T");
Clazz.defineMethod (c$, "addOpAllowMath", 
function (op, allowMathFunc) {
if (this.debugHigh) {
this.dumpStacks ("adding " + op + " wasx=" + this.wasX);
}var tok0 = (this.oPt >= 0 && this.oStack[this.oPt] != null ? this.oStack[this.oPt].tok : 0);
this.skipping = (this.ifPt >= 0 && (this.ifStack[this.ifPt] == 'F' || this.ifStack[this.ifPt] == 'X'));
if (this.skipping) return this.checkSkip (op, tok0);
var tok;
var isDotSelector = (op.tok == 269484241);
if (isDotSelector && !this.wasX) return false;
var isMathFunc = (allowMathFunc && JS.ScriptMathProcessor.isOpFunc (op));
if (this.oPt >= 1 && op.tok != 269484048 && tok0 == 135266319) tok0 = this.oStack[--this.oPt].tok;
var newOp = null;
var isLeftOp = false;
switch (op.tok) {
case 1073742195:
this.haveSpaceBeforeSquare = true;
return true;
case 269484080:
if (!this.wasX) return false;
break;
case 269484225:
case 269484226:
if (this.wasX && op.intValue == -1 && this.addOp (JS.T.tokenComma)) return this.addOp (op);
break;
case 269484097:
break;
case 269484049:
if (!this.wasX && this.oPt >= 1 && tok0 == 269484048 && !JS.ScriptMathProcessor.isOpFunc (this.oStack[this.oPt - 1])) return false;
break;
case 269484192:
if (!this.wasX) op = JS.SV.newV (269484224, "-");
break;
case 32:
case 64:
case 96:
case 128:
case 160:
case 192:
case 480:
tok = (this.oPt < 0 ? 0 : tok0);
if (!this.wasX || !(tok == 269484241 || tok == 1678770178 || tok == 1141899265)) return false;
this.oStack[this.oPt].intValue |= op.tok;
return true;
case 269484096:
isLeftOp = true;
if (!this.wasX || this.haveSpaceBeforeSquare) {
this.squareCount++;
op = newOp = JS.T.tokenArraySquare;
this.haveSpaceBeforeSquare = false;
}break;
case 269484144:
case 269484048:
isLeftOp = true;
default:
if (isMathFunc) {
var isArgument = (this.oPt >= 1 && tok0 == 269484048);
if (!isDotSelector && this.wasX && !isArgument) return false;
newOp = op;
isLeftOp = true;
break;
}if (this.wasX == isLeftOp && tok0 != 269484241) {
if (!this.wasX || !allowMathFunc) return false;
if (this.addOp (JS.T.tokenComma)) return this.addOp (op);
}break;
}
while (this.oPt >= 0 && tok0 != 269484066 && (op.tok != 269484225 && op.tok != 269484226 || this.wasX) && (!isLeftOp || tok0 == 269484241 && (op.tok == 269484241 || op.tok == 269484096)) && JS.T.getPrecedence (tok0) >= JS.T.getPrecedence (op.tok) && (tok0 != 269484224 || op.tok != 269484224)) {
if (op.tok == 269484049 && tok0 == 269484048) {
if (this.xPt >= 0) this.xStack[this.xPt] = JS.SV.selectItemVar (this.xStack[this.xPt]);
this.wasX = true;
break;
}if (op.tok == 269484097 && tok0 == 135266306) {
break;
}if (op.tok == 269484097 && tok0 == 269484096) {
if (this.isArrayItem && this.squareCount == 1 && this.equalCount == 0) {
this.wasX = false;
this.addX (JS.SV.newT (JS.T.tokenArraySelector));
break;
}if (!this.doSelection ()) return false;
this.wasX = true;
break;
}if (!this.operate ()) return false;
tok0 = (this.oPt >= 0 && this.oStack[this.oPt] != null ? this.oStack[this.oPt].tok : 0);
}
if (newOp != null) {
this.wasX = false;
this.addX (JS.SV.newV (269484436, newOp));
}switch (op.tok) {
case 269484048:
this.parenCount++;
this.wasX = false;
break;
case 806354977:
var isFirst = this.getX ().asBoolean ();
if (tok0 == 269484066) this.ifPt--;
 else this.putOp (JS.T.tokenColon);
this.putIf (isFirst ? 'T' : 'F');
this.skipping = !isFirst;
this.wasX = false;
return true;
case 269484066:
if (tok0 != 269484066) return false;
if (this.ifPt < 0) return false;
this.ifStack[this.ifPt] = 'X';
this.wasX = false;
this.skipping = true;
return true;
case 269484049:
this.wasX = true;
if (this.parenCount-- <= 0) return false;
if (tok0 == 269484066) {
this.ifPt--;
this.oPt--;
}this.oPt--;
if (this.oPt < 0) return true;
if (JS.ScriptMathProcessor.isOpFunc (this.oStack[this.oPt])) {
this.wasX = false;
if (!this.evaluateFunction (0)) return false;
}this.skipping = (this.ifPt >= 0 && this.ifStack[this.ifPt] == 'X');
return true;
case 269484080:
this.wasX = false;
return true;
case 269484096:
this.squareCount++;
this.wasX = false;
break;
case 269484097:
this.wasX = true;
if (this.squareCount-- <= 0 || this.oPt < 0 || !this.doSelections) return !this.doSelections;
if (this.oStack[this.oPt].tok == 135266306) return this.evaluateFunction (269484096);
this.oPt--;
return true;
case 269484241:
this.wasX = (!allowMathFunc || !JS.T.tokAttr (op.intValue, 135266304));
break;
case 1048586:
this.braceCount++;
this.wasX = false;
break;
case 1048590:
if (this.braceCount-- <= 0) return false;
this.wasX = false;
break;
case 269484128:
case 269484112:
if (!this.wasSyntaxCheck && this.xPt < 0) return false;
if (!this.wasSyntaxCheck && this.xStack[this.xPt].tok != 10 && this.xStack[this.xPt].tok != 7) {
var tf = this.getX ().asBoolean ();
this.addX (JS.SV.getBoolean (tf));
if (tf == (op.tok == 269484112)) {
this.chk = true;
op = (op.tok == 269484112 ? JS.T.tokenOrTRUE : JS.T.tokenAndFALSE);
}}this.wasX = false;
break;
case 269484226:
case 269484225:
break;
case 269484436:
if (this.squareCount == 0) {
this.doSelections = true;
this.assignLeft = false;
this.equalCount++;
}this.wasX = false;
break;
default:
this.wasX = false;
}
this.putOp (op);
switch (op.tok) {
case 269484241:
return (((op.intValue & -481) == 135368713 && op.intValue != 135368713) ? this.evaluateFunction (0) : true);
case 269484226:
case 269484225:
return (this.wasX ? this.operate () : true);
}
return true;
}, "JS.T,~B");
Clazz.defineMethod (c$, "checkSkip", 
 function (op, tok0) {
switch (op.tok) {
case 269484048:
this.putOp (op);
break;
case 269484066:
if (tok0 != 269484066 || this.ifStack[this.ifPt] == 'X') break;
this.ifStack[this.ifPt] = 'T';
this.wasX = false;
this.skipping = false;
break;
case 269484049:
if (tok0 == 269484048) {
this.oPt--;
break;
}if (tok0 != 269484066) {
this.putOp (op);
break;
}this.wasX = true;
this.ifPt--;
this.oPt -= 2;
this.skipping = false;
break;
}
return true;
}, "JS.T,~N");
Clazz.defineMethod (c$, "doSelection", 
 function () {
if (this.xPt < 0 || this.xPt == 0 && !this.isArrayItem) {
return false;
}var var1 = this.xStack[this.xPt--];
var $var = this.xStack[this.xPt];
if (($var.tok == 7 || $var.tok == 15) && $var.intValue != 2147483647) if (var1.tok == 4 || this.assignLeft && this.squareCount == 1) {
this.xStack[this.xPt] = $var = JS.SV.selectItemTok ($var, -2147483648);
}if (this.assignLeft && $var.tok != 4) this.lastAssignedString = null;
switch ($var.tok) {
case 6:
case 14:
if (this.doSelections) {
var v = $var.mapValue (JS.SV.sValue (var1));
this.xStack[this.xPt] = (v == null ? JS.SV.newS ("") : v);
} else {
this.xPt++;
this.putOp (null);
}return true;
default:
$var = JS.SV.newS (JS.SV.sValue ($var));
case 10:
case 15:
case 7:
case 4:
case 11:
case 12:
if (this.doSelections || $var.tok == 7 && $var.intValue == 2147483647) {
this.xStack[this.xPt] = JS.SV.selectItemTok ($var, var1.asInt ());
if (this.assignLeft && $var.tok == 4 && this.squareCount == 1) this.lastAssignedString = $var;
} else {
this.xPt++;
}if (!this.doSelections) this.putOp (null);
break;
}
return true;
});
Clazz.defineMethod (c$, "dumpStacks", 
function (message) {
JU.Logger.debug ("\n\n------------------\nRPN stacks: " + message + "\n");
for (var i = 0; i <= this.xPt; i++) JU.Logger.debug ("x[" + i + "]: " + this.xStack[i]);

JU.Logger.debug ("\n");
for (var i = 0; i <= this.oPt; i++) JU.Logger.debug ("o[" + i + "]: " + this.oStack[i] + " prec=" + (this.oStack[i] == null ? "--" : "" + JS.T.getPrecedence (this.oStack[i].tok)));

JU.Logger.debug (" ifStack = " + ( String.instantialize (this.ifStack)).substring (0, this.ifPt + 1));
}, "~S");
Clazz.defineMethod (c$, "getX", 
function () {
if (this.xPt < 0) this.eval.error (13);
var v = JS.SV.selectItemVar (this.xStack[this.xPt]);
this.xStack[this.xPt--] = null;
this.wasX = false;
return v;
});
Clazz.defineMethod (c$, "evaluateFunction", 
 function (tok) {
var op = this.oStack[this.oPt--];
if (tok == 0) tok = (op.tok == 269484241 ? op.intValue & -481 : op.tok);
var nParamMax = JS.T.getMaxMathParams (tok);
var nParam = 0;
var pt = this.xPt;
while (pt >= 0 && this.xStack[pt--].value !== op) nParam++;

if (nParamMax > 0 && nParam > nParamMax) return false;
var args =  new Array (nParam);
for (var i = nParam; --i >= 0; ) args[i] = this.getX ();

this.xPt--;
if (!this.chk) return this.getMathExt ().evaluate (this, op, args, tok);
if (op.tok == 269484241) this.xPt--;
return this.addXBool (true);
}, "~N");
Clazz.defineMethod (c$, "operate", 
 function () {
var op = this.oStack[this.oPt--];
var pt;
var m;
var m4;
var s;
var x1;
if (this.debugHigh) {
this.dumpStacks ("operate: " + op);
}if (op.tok == 269484436 && (this.isArrayItem && this.squareCount == 0 && this.equalCount == 1 && this.oPt < 0 || this.oPt >= 0 && this.oStack[this.oPt] == null)) return true;
var x2 = this.getX ();
if (x2 === JS.T.tokenArraySelector) return false;
switch (op.tok) {
case 269484225:
case 269484226:
x1 = x2;
if (!this.chk) {
if (this.ptx < this.pto) {
x1 = JS.SV.newS ("").setv (x2);
}if (!x2.increment (op.tok == 269484226 ? 1 : -1)) return false;
if (this.ptx > this.pto) {
x1 = JS.SV.newS ("").setv (x2);
}}this.wasX = false;
this.putX (x1);
this.wasX = true;
return true;
case 269484224:
switch (x2.tok) {
case 2:
return this.addXInt (-x2.asInt ());
case 8:
pt = JU.P3.newP (x2.value);
pt.scale (-1.0);
return this.addXPt (pt);
case 9:
var pt4 = JU.P4.newPt (x2.value);
pt4.scale4 (-1.0);
return this.addXPt4 (pt4);
case 11:
m = JU.M3.newM3 (x2.value);
m.transpose ();
return this.addXM3 (m);
case 12:
m4 = JU.M4.newM4 (x2.value);
m4.transpose ();
return this.addXM4 (m4);
case 10:
return this.addXBs (JU.BSUtil.copyInvert (JS.SV.bsSelectVar (x2), (Clazz.instanceOf (x2.value, JM.BondSet) ? this.vwr.ms.bondCount : this.vwr.ms.ac)));
}
return this.addXFloat (-x2.asFloat ());
case 269484144:
if (this.chk) return this.addXBool (true);
switch (x2.tok) {
case 9:
return this.addXPt4 ((JU.Quat.newP4 (x2.value)).inv ().toPoint4f ());
case 11:
m = JU.M3.newM3 (x2.value);
m.invert ();
return this.addXM3 (m);
case 12:
m4 = JU.M4.newM4 (x2.value);
m4.invert ();
return this.addXM4 (m4);
case 10:
return this.addXBs (JU.BSUtil.copyInvert (JS.SV.bsSelectVar (x2), (Clazz.instanceOf (x2.value, JM.BondSet) ? this.vwr.ms.bondCount : this.vwr.ms.ac)));
default:
return this.addXBool (!x2.asBoolean ());
}
case 269484241:
var iv = op.intValue & -481;
if (this.chk) return this.addXObj (JS.SV.newS (""));
if (this.vwr.allowArrayDotNotation) switch (x2.tok) {
case 6:
case 14:
switch (iv) {
case 1141899272:
case 1141899282:
case 1141899270:
break;
default:
var ret = x2.mapValue (op.value);
return this.addXObj (ret == null ? JS.SV.newS ("") : ret);
}
break;
}
switch (iv) {
case 1073741824:
return (x2.tok == 10 && this.getAllProperties (x2, op.value));
case 1141899272:
return this.addXStr (JS.ScriptMathProcessor.typeOf (x2));
case 1141899282:
return this.getKeys (x2, (op.intValue & 480) == 480);
case 1141899267:
case 1276117012:
case 1141899270:
if (iv == 1141899267 && Clazz.instanceOf (x2.value, JM.BondSet)) break;
return this.addXInt (JS.SV.sizeOf (x2));
case 1141899268:
switch (x2.tok) {
case 11:
case 12:
s = JS.SV.sValue (x2);
s = JU.PT.rep (s.substring (1, s.length - 1), "],[", "]\n[");
break;
case 4:
s = x2.value;
break;
default:
s = JS.SV.sValue (x2);
}
s = JU.PT.rep (s, "\n\r", "\n").$replace ('\r', '\n');
return this.addXAS (JU.PT.split (s, "\n"));
case 1766856708:
switch (x2.tok) {
case 4:
case 7:
return this.addXPt (JU.CU.colorPtFromString (JS.SV.sValue (x2)));
case 2:
case 3:
return this.addXPt (this.vwr.getColorPointForPropertyValue (JS.SV.fValue (x2)));
case 8:
return this.addXStr (JU.Escape.escapeColor (JU.CU.colorPtToFFRGB (x2.value)));
default:
}
break;
case 1679429641:
return (this.chk ? this.addXStr ("x") : this.getBoundBox (x2));
}
if (this.chk) return this.addXStr (JS.SV.sValue (x2));
if (x2.tok == 4) {
var v = JS.SV.unescapePointOrBitsetAsVariable (JS.SV.sValue (x2));
if (!(Clazz.instanceOf (v, JS.SV))) return false;
x2 = v;
}if (op.tok == x2.tok) x2 = this.getX ();
return this.getPointOrBitsetOperation (op, x2);
}
x1 = this.getX ();
if (this.chk) {
if (op === JS.T.tokenAndFALSE || op === JS.T.tokenOrTRUE) this.chk = false;
return this.addX (JS.SV.newT (x1));
}return this.binaryOp (op, x1, x2);
});
Clazz.defineMethod (c$, "getKeys", 
 function (x2, isAll) {
switch (x2.tok) {
case 6:
case 14:
case 7:
break;
default:
return this.addXStr ("");
}
var keys =  new JU.Lst ();
this.getKeyList (x2, isAll, keys, "");
var skeys = keys.toArray ( new Array (keys.size ()));
java.util.Arrays.sort (skeys);
return this.addXAS (skeys);
}, "JS.SV,~B");
Clazz.defineMethod (c$, "getKeyList", 
 function (x2, isAll, keys, prefix) {
var map = x2.getMap ();
if (map == null) {
if (isAll) {
var lst;
var n;
if ((lst = x2.getList ()) != null && (n = lst.size ()) > 0) this.getKeyList (lst.get (n - 1), true, keys, prefix + n + ".");
}return;
}for (var e, $e = map.entrySet ().iterator (); $e.hasNext () && ((e = $e.next ()) || true);) {
var k = e.getKey ();
if (isAll && (k.length == 0 || !JU.PT.isLetter (k.charAt (0)))) {
if (prefix.endsWith (".")) prefix = prefix.substring (0, prefix.length - 1);
k = "[" + JU.PT.esc (k) + "]";
}keys.addLast (prefix + k);
if (isAll) this.getKeyList (e.getValue (), true, keys, prefix + k + ".");
}
}, "JS.SV,~B,JU.Lst,~S");
Clazz.defineMethod (c$, "binaryOp", 
function (op, x1, x2) {
var pt;
var pt4;
var m;
var s;
var f;
switch (op.tok) {
case 269484160:
case 269484128:
switch (x1.tok) {
case 10:
var bs = JS.SV.bsSelectVar (x1);
switch (x2.tok) {
case 2:
var x = x2.asInt ();
return (this.addXBool (x < 0 ? false : bs.get (x)));
case 10:
bs = JU.BSUtil.copy (bs);
bs.and (JS.SV.bsSelectVar (x2));
return this.addXBs (bs);
}
break;
}
return this.addXBool (x1.asBoolean () && x2.asBoolean ());
case 269484112:
switch (x1.tok) {
case 10:
var bs = JU.BSUtil.copy (JS.SV.bsSelectVar (x1));
switch (x2.tok) {
case 10:
bs.or (JS.SV.bsSelectVar (x2));
return this.addXBs (bs);
case 2:
var x = x2.asInt ();
if (x < 0) break;
bs.set (x);
return this.addXBs (bs);
case 7:
var sv = x2.value;
for (var i = sv.size (); --i >= 0; ) {
var b = sv.get (i).asInt ();
if (b >= 0) bs.set (b);
}
return this.addXBs (bs);
}
break;
case 7:
return this.addX (JS.SV.concatList (x1, x2, false));
}
return this.addXBool (x1.asBoolean () || x2.asBoolean ());
case 269484113:
if (x1.tok == 10 && x2.tok == 10) {
var bs = JU.BSUtil.copy (JS.SV.bsSelectVar (x1));
bs.xor (JS.SV.bsSelectVar (x2));
return this.addXBs (bs);
}var a = x1.asBoolean ();
var b = x2.asBoolean ();
return this.addXBool (a && !b || b && !a);
case 269484114:
if (x1.tok != 10 || x2.tok != 10) return false;
return this.addXBs (JU.BSUtil.toggleInPlace (JU.BSUtil.copy (JS.SV.bsSelectVar (x1)), JS.SV.bsSelectVar (x2)));
case 269484434:
return this.addXBool (x1.asFloat () <= x2.asFloat ());
case 269484433:
return this.addXBool (x1.asFloat () >= x2.asFloat ());
case 269484432:
return this.addXBool (x1.asFloat () > x2.asFloat ());
case 269484435:
return this.addXBool (x1.asFloat () < x2.asFloat ());
case 269484436:
return this.addXBool (JS.SV.areEqual (x1, x2));
case 269484437:
return this.addXBool (!JS.SV.areEqual (x1, x2));
case 269484438:
return this.addXBool (JS.SV.isLike (x1, x2));
case 269484193:
switch (x1.tok) {
case 2:
if (!this.isDecimal (x2)) return this.addXInt (x1.intValue + x2.asInt ());
break;
case 4:
return this.addX (JS.SV.newS (JS.SV.sValue (x1) + JS.SV.sValue (x2)));
case 8:
pt = JU.P3.newP (x1.value);
switch (x2.tok) {
case 8:
pt.add (x2.value);
return this.addXPt (pt);
case 9:
pt4 = x2.value;
pt.add (JU.P3.new3 (pt4.x, pt4.y, pt4.z));
return this.addXPt (pt);
default:
f = x2.asFloat ();
return this.addXPt (JU.P3.new3 (pt.x + f, pt.y + f, pt.z + f));
}
case 11:
switch (x2.tok) {
default:
return this.addXFloat (x1.asFloat () + x2.asFloat ());
case 11:
m = JU.M3.newM3 (x1.value);
m.add (x2.value);
return this.addXM3 (m);
case 8:
return this.addXM4 (JS.ScriptMathProcessor.getMatrix4f (x1.value, x2.value));
}
case 9:
var q1 = JU.Quat.newP4 (x1.value);
switch (x2.tok) {
default:
return this.addXPt4 (q1.add (x2.asFloat ()).toPoint4f ());
case 9:
return this.addXPt4 (q1.mulQ (JU.Quat.newP4 (x2.value)).toPoint4f ());
}
case 7:
return this.addX (JS.SV.concatList (x1, x2, true));
}
return this.addXFloat (x1.asFloat () + x2.asFloat ());
case 269484192:
switch (x1.tok) {
case 2:
if (!this.isDecimal (x2)) return this.addXInt (x1.intValue - x2.asInt ());
break;
case 4:
if (!this.isDecimal (x2) && !this.isDecimal (x1)) return this.addXInt (x1.asInt () - x2.asInt ());
break;
case 6:
var ht =  new java.util.Hashtable (x1.value);
ht.remove (JS.SV.sValue (x2));
return this.addX (JS.SV.getVariableMap (ht));
case 11:
if (x2.tok != 11) break;
m = JU.M3.newM3 (x1.value);
m.sub (x2.value);
return this.addXM3 (m);
case 12:
if (x2.tok != 12) break;
var m4 = JU.M4.newM4 (x1.value);
m4.sub (x2.value);
return this.addXM4 (m4);
case 8:
pt = JU.P3.newP (x1.value);
switch (x2.tok) {
case 8:
pt.sub (x2.value);
return this.addXPt (pt);
case 9:
pt4 = x2.value;
pt.sub (JU.P3.new3 (pt4.x, pt4.y, pt4.z));
return this.addXPt (pt);
}
f = x2.asFloat ();
return this.addXPt (JU.P3.new3 (pt.x - f, pt.y - f, pt.z - f));
case 9:
var q1 = JU.Quat.newP4 (x1.value);
if (x2.tok == 9) {
var q2 = JU.Quat.newP4 (x2.value);
return this.addXPt4 (q2.mulQ (q1.inv ()).toPoint4f ());
}return this.addXPt4 (q1.add (-x2.asFloat ()).toPoint4f ());
}
return this.addXFloat (x1.asFloat () - x2.asFloat ());
case 1276117508:
if (x1.tok == 8 && x2.tok == 8) {
pt = x1.value;
var pt2 = x2.value;
return this.addXPt (JU.P3.new3 (pt.x * pt2.x, pt.y * pt2.y, pt.z * pt2.z));
}case 269484209:
switch (x1.tok) {
case 2:
return (this.isDecimal (x2) ? this.addXFloat (x1.intValue * x2.asFloat ()) : this.addXInt (x1.intValue * x2.asInt ()));
case 4:
return (this.isDecimal (x2) || this.isDecimal (x1) ? this.addXFloat (x1.asFloat () * x2.asFloat ()) : this.addXInt (x1.asInt () * x2.asInt ()));
}
pt = (x1.tok == 11 ? this.ptValue (x2, false) : x2.tok == 11 ? this.ptValue (x1, false) : null);
pt4 = (x1.tok == 12 ? this.planeValue (x2) : x2.tok == 12 ? this.planeValue (x1) : null);
switch (x2.tok) {
case 11:
if (pt != null) {
var m3b = JU.M3.newM3 (x2.value);
m3b.transpose ();
m3b.rotate (pt);
if (x1.tok == 7) return this.addX (JS.SV.getVariableAF ([pt.x, pt.y, pt.z]));
return this.addXPt (pt);
}if (pt4 != null) return this.addXPt4 ((JU.Quat.newP4 (pt4).mulQ (JU.Quat.newM (x2.value))).toPoint4f ());
break;
case 12:
if (pt4 != null) {
var m4b = JU.M4.newM4 (x2.value);
m4b.transpose ();
m4b.transform (pt4);
if (x1.tok == 7) return this.addX (JS.SV.getVariableAF ([pt4.x, pt4.y, pt4.z, pt4.w]));
return this.addXPt4 (pt4);
}break;
}
switch (x1.tok) {
case 11:
var m3 = x1.value;
if (pt != null) {
m3.rotate (pt);
if (x2.tok == 7) return this.addX (JS.SV.getVariableAF ([pt.x, pt.y, pt.z]));
return this.addXPt (pt);
}switch (x2.tok) {
case 11:
m = JU.M3.newM3 (x2.value);
m.mul2 (m3, m);
return this.addXM3 (m);
case 9:
return this.addXM3 (JU.Quat.newM (m3).mulQ (JU.Quat.newP4 (x2.value)).getMatrix ());
}
f = x2.asFloat ();
var aa =  new JU.A4 ();
aa.setM (m3);
aa.angle *= f;
return this.addXM3 ( new JU.M3 ().setAA (aa));
case 12:
var m4 = x1.value;
if (pt != null) {
m4.rotTrans (pt);
if (x2.tok == 7) return this.addX (JS.SV.getVariableAF ([pt.x, pt.y, pt.z]));
return this.addXPt (pt);
}if (pt4 != null) {
m4.transform (pt4);
if (x2.tok == 7) return this.addX (JS.SV.getVariableAF ([pt4.x, pt4.y, pt4.z, pt4.w]));
return this.addXPt4 (pt4);
}if (x2.tok == 12) {
var m4b = JU.M4.newM4 (x2.value);
m4b.mul2 (m4, m4b);
return this.addXM4 (m4b);
}return this.addXStr ("NaN");
case 8:
pt = JU.P3.newP (x1.value);
switch (x2.tok) {
case 8:
var pt2 = (x2.value);
return this.addXFloat (pt.x * pt2.x + pt.y * pt2.y + pt.z * pt2.z);
}
f = x2.asFloat ();
return this.addXPt (JU.P3.new3 (pt.x * f, pt.y * f, pt.z * f));
case 9:
if (x2.tok == 9) return this.addXPt4 (JU.Quat.newP4 (x1.value).mulQ (JU.Quat.newP4 (x2.value)).toPoint4f ());
return this.addXPt4 (JU.Quat.newP4 (x1.value).mul (x2.asFloat ()).toPoint4f ());
}
return this.addXFloat (x1.asFloat () * x2.asFloat ());
case 269484208:
var f2;
switch (x1.tok) {
case 2:
if (x2.tok == 2 && x2.intValue != 0) return this.addXInt (Clazz.doubleToInt (x1.intValue / x2.intValue));
var n = (this.isDecimal (x2) ? 0 : x2.asInt ());
if (n != 0) return this.addXInt (Clazz.doubleToInt (x1.intValue / n));
break;
case 4:
var i2;
if (!this.isDecimal (x1) && !this.isDecimal (x2) && (i2 = x2.asInt ()) != 0) return this.addXInt (Clazz.doubleToInt (x1.asInt () / i2));
break;
case 8:
pt = JU.P3.newP (x1.value);
return this.addXPt ((f2 = x2.asFloat ()) == 0 ? JU.P3.new3 (NaN, NaN, NaN) : JU.P3.new3 (pt.x / f2, pt.y / f2, pt.z / f2));
case 9:
return this.addXPt4 (x2.tok == 9 ? JU.Quat.newP4 (x1.value).div (JU.Quat.newP4 (x2.value)).toPoint4f () : (f2 = x2.asFloat ()) == 0 ? JU.P4.new4 (NaN, NaN, NaN, NaN) : JU.Quat.newP4 (x1.value).mul (1 / f2).toPoint4f ());
}
return this.addXFloat (x1.asFloat () / x2.asFloat ());
case 269484211:
f = x2.asFloat ();
if (x1.tok == 9) {
if (f == 0) return this.addXPt4 (JU.P4.new4 (NaN, NaN, NaN, NaN));
if (x2.tok == 9) return this.addXPt4 (JU.Quat.newP4 (x1.value).divLeft (JU.Quat.newP4 (x2.value)).toPoint4f ());
return this.addXPt4 (JU.Quat.newP4 (x1.value).mul (1 / f).toPoint4f ());
}return this.addXInt (f == 0 ? 0 : Clazz.doubleToInt (Math.floor (x1.asFloat () / x2.asFloat ())));
case 269484227:
f = Math.pow (x1.asFloat (), x2.asFloat ());
return (x1.tok == 2 && x2.tok == 2 ? this.addXInt (Clazz.floatToInt (f)) : this.addXFloat (f));
case 269484210:
s = null;
var n = x2.asInt ();
switch (x1.tok) {
case 1048589:
case 1048588:
case 2:
default:
break;
case 3:
f = x1.asFloat ();
if (n == 0) return this.addXInt (Math.round (f));
s = JU.DF.formatDecimal (f, n);
return this.addXStr (s);
case 4:
s = x1.value;
if (n == 0) return this.addXStr (JU.PT.trim (s, "\n\t "));
if (n == 9999) return this.addXStr (s.toUpperCase ());
if (n == -9999) return this.addXStr (s.toLowerCase ());
if (n > 0) return this.addXStr (JU.PT.formatS (s, n, n, false, false));
return this.addXStr (JU.PT.formatS (s, n, n - 1, true, false));
case 7:
var list = JS.SV.strListValue (x1);
for (var i = 0; i < list.length; i++) {
if (n == 0) list[i] = list[i].trim ();
 else if (n > 0) list[i] = JU.PT.formatS (list[i], n, n, true, false);
 else list[i] = JU.PT.formatS (s, -n, n, false, false);
}
return this.addXAS (list);
case 8:
pt = JU.P3.newP (x1.value);
this.vwr.toUnitCell (pt, JU.P3.new3 (n, n, n));
return this.addXPt (pt);
case 9:
pt4 = x1.value;
if (x2.tok == 8) return this.addXPt ((JU.Quat.newP4 (pt4)).transform2 (x2.value,  new JU.P3 ()));
if (x2.tok == 9) {
var v4 = JU.P4.newPt (x2.value);
(JU.Quat.newP4 (pt4)).getThetaDirected (v4);
return this.addXPt4 (v4);
}if (n == 0 && x2.tok == 4) {
s = " " + x2.value.toString ().trim ().toLowerCase () + ":";
var i = " w:0 x:1 y:2 z:3 normal:4 eulerzxz:5 eulerzyz:6 vector:-1 theta:-2 axisx:-3 axisy:-4 axisz:-5 axisangle:-6 matrix:-9".indexOf (s);
n = (i >= 0 ? JU.PT.parseInt (" w:0 x:1 y:2 z:3 normal:4 eulerzxz:5 eulerzyz:6 vector:-1 theta:-2 axisx:-3 axisy:-4 axisz:-5 axisangle:-6 matrix:-9".substring (i + s.length)) : -99);
}switch (n) {
case 0:
return this.addXFloat (pt4.w);
case 1:
return this.addXFloat (pt4.x);
case 2:
return this.addXFloat (pt4.y);
case 3:
return this.addXFloat (pt4.z);
}
var q = JU.Quat.newP4 (pt4);
switch (n) {
case 4:
return this.addXPt (JU.P3.newP (q.getNormal ()));
case 5:
return this.addXAF (q.getEulerZXZ ());
case 6:
return this.addXAF (q.getEulerZYZ ());
case -1:
return this.addXPt (JU.P3.newP (q.getVector (-1)));
case -2:
return this.addXFloat (q.getTheta ());
case -3:
return this.addXPt (JU.P3.newP (q.getVector (0)));
case -4:
return this.addXPt (JU.P3.newP (q.getVector (1)));
case -5:
return this.addXPt (JU.P3.newP (q.getVector (2)));
case -6:
var ax = q.toAxisAngle4f ();
return this.addXPt4 (JU.P4.new4 (ax.x, ax.y, ax.z, (ax.angle * 180 / 3.141592653589793)));
case -9:
return this.addXM3 (q.getMatrix ());
default:
return this.addXStr ("NaN");
}
case 12:
var m4 = x1.value;
switch (n) {
case 1:
var m3 =  new JU.M3 ();
m4.getRotationScale (m3);
return this.addXM3 (m3);
case 2:
var v3 =  new JU.V3 ();
m4.getTranslation (v3);
return this.addXPt (JU.P3.newP (v3));
default:
return false;
}
case 10:
return this.addXBs (JS.SV.bsSelectRange (x1, n));
}
return this.addXInt (n == 0 ? 0 : x1.asInt () % n);
}
return true;
}, "JS.T,JS.SV,JS.SV");
Clazz.defineMethod (c$, "isDecimal", 
 function (x) {
var s;
return (x.tok == 3 || x.tok == 4 && ((s = JS.SV.sValue (x).trim ()).indexOf (".") >= 0 || s.indexOf ("+") > 0 || s.lastIndexOf ("-") > 0));
}, "JS.SV");
Clazz.defineMethod (c$, "ptValue", 
function (x, allowFloat) {
var pt;
if (this.chk) return  new JU.P3 ();
switch (x.tok) {
case 8:
return x.value;
case 10:
return this.eval.getBitsetProperty (JS.SV.bsSelectVar (x), 1146095626, null, null, x.value, null, false, 2147483647, false);
case 4:
pt = JU.Escape.uP (JS.SV.sValue (x));
if (Clazz.instanceOf (pt, JU.P3)) return pt;
break;
case 7:
pt = JU.Escape.uP ("{" + JS.SV.sValue (x).$replace (']', ' ').$replace ('[', ' ') + "}");
if (Clazz.instanceOf (pt, JU.P3)) return pt;
break;
}
if (!allowFloat) return null;
var f = JS.SV.fValue (x);
return JU.P3.new3 (f, f, f);
}, "JS.SV,~B");
Clazz.defineMethod (c$, "planeValue", 
function (x) {
if (this.chk) return  new JU.P4 ();
switch (x.tok) {
case 9:
return x.value;
case 7:
case 4:
var pt = JU.Escape.uP (JS.SV.sValue (x));
return (Clazz.instanceOf (pt, JU.P4) ? pt : null);
case 10:
break;
}
return null;
}, "JS.T");
c$.typeOf = Clazz.defineMethod (c$, "typeOf", 
 function (x) {
var tok = (x == null ? 0 : x.tok);
switch (tok) {
case 1048589:
case 1048588:
return "boolean";
case 10:
return (Clazz.instanceOf (x.value, JM.BondSet) ? "bondset" : "bitset");
case 2:
case 3:
case 8:
case 9:
case 4:
case 7:
case 6:
case 15:
case 11:
case 12:
case 14:
return JS.T.astrType[tok];
}
return "?";
}, "JS.SV");
Clazz.defineMethod (c$, "getAllProperties", 
 function (x2, abbr) {
if (this.chk) return this.addXStr ("");
var bs = JS.SV.bsSelectVar (x2);
var tokens;
var n = bs.cardinality ();
if (n == 0 || (tokens = JS.T.getAtomPropertiesLike (abbr.substring (0, abbr.length - 1))) == null) return this.addXStr ("");
var ht =  new java.util.Hashtable ();
var index = (n == 1 ? bs.nextSetBit (0) : 2147483647);
for (var i = tokens.size (); --i >= 0; ) {
var t = tokens.get (i);
var tok = t.tok;
switch (tok) {
case 1095766024:
case 1095761925:
continue;
default:
if (index == 2147483647) tok |= 480;
ht.put (t.value, JS.SV.getVariable (this.eval.getBitsetProperty (bs, tok, null, null, null, null, false, index, true)));
}
}
return this.addXMap (ht);
}, "JS.SV,~S");
c$.getMatrix4f = Clazz.defineMethod (c$, "getMatrix4f", 
function (matRotate, vTranslate) {
return JU.M4.newMV (matRotate, vTranslate == null ?  new JU.V3 () : JU.V3.newV (vTranslate));
}, "JU.M3,JU.T3");
Clazz.defineMethod (c$, "getBoundBox", 
 function (x2) {
if (x2.tok != 10) return false;
if (this.chk) return this.addXStr ("");
var b = this.vwr.ms.getBoxInfo (JS.SV.bsSelectVar (x2), 1);
var pts = b.getBoundBoxPoints (true);
var list =  new JU.Lst ();
for (var i = 0; i < 4; i++) list.addLast (pts[i]);

return this.addXList (list);
}, "JS.SV");
Clazz.defineMethod (c$, "getPointOrBitsetOperation", 
 function (op, x2) {
switch (x2.tok) {
case 7:
switch (op.intValue) {
case 32:
case 64:
case 96:
case 192:
case 128:
case 160:
return this.addXObj (this.getMathExt ().getMinMax (x2.getList (), op.intValue));
case 1276383249:
return this.addX (x2.pushPop (null, null));
case 1276117011:
case 1141899269:
return this.addX (x2.sortOrReverse (op.intValue == 1141899269 ? -2147483648 : 1));
}
var list2 =  new Array (x2.getList ().size ());
for (var i = 0; i < list2.length; i++) {
var v = JS.SV.unescapePointOrBitsetAsVariable (x2.getList ().get (i));
if (!(Clazz.instanceOf (v, JS.SV)) || !this.getPointOrBitsetOperation (op, v)) return false;
list2[i] = this.xStack[this.xPt--];
}
return this.addXAV (list2);
case 8:
switch (op.intValue) {
case 1112541185:
case 1112541205:
return this.addXFloat ((x2.value).x);
case 1112541186:
case 1112541206:
return this.addXFloat ((x2.value).y);
case 1112541187:
case 1112541207:
return this.addXFloat ((x2.value).z);
case 1146095626:
var pt = JU.P3.newP (x2.value);
this.vwr.toCartesian (pt, true);
return this.addXPt (pt);
case 1112541188:
case 1112541189:
case 1112541190:
case 1146095627:
var ptf = JU.P3.newP (x2.value);
this.vwr.toFractional (ptf, true);
return (op.intValue == 1146095627 ? this.addXPt (ptf) : this.addXFloat (op.intValue == 1112541188 ? ptf.x : op.intValue == 1112541189 ? ptf.y : ptf.z));
case 1112541191:
case 1112541192:
case 1112541193:
case 1146095629:
var ptfu = JU.P3.newP (x2.value);
this.vwr.toFractional (ptfu, false);
return (op.intValue == 1146095629 ? this.addXPt (ptfu) : this.addXFloat (op.intValue == 1112541191 ? ptfu.x : op.intValue == 1112541192 ? ptfu.y : ptfu.z));
case 1112539153:
case 1112539154:
case 1112539155:
case 1146093582:
var ptu = JU.P3.newP (x2.value);
this.vwr.toUnitCell (ptu, null);
this.vwr.toFractional (ptu, false);
return (op.intValue == 1146093582 ? this.addXPt (ptu) : this.addXFloat (op.intValue == 1112539153 ? ptu.x : op.intValue == 1112539154 ? ptu.y : ptu.z));
}
break;
case 9:
switch (op.intValue) {
case 1112541185:
case 1112541205:
return this.addXFloat ((x2.value).x);
case 1112541186:
case 1112541206:
return this.addXFloat ((x2.value).y);
case 1112541187:
case 1112541207:
return this.addXFloat ((x2.value).z);
case 1141899281:
return this.addXFloat ((x2.value).w);
}
break;
case 10:
if (op.intValue == 1678770178 && Clazz.instanceOf (x2.value, JM.BondSet)) return this.addX (x2);
var bs = JS.SV.bsSelectVar (x2);
if (bs.cardinality () == 1 && (op.intValue & 480) == 0) op.intValue |= 32;
var val = this.eval.getBitsetProperty (bs, op.intValue, null, null, x2.value, op.value, false, x2.index, true);
if (op.intValue != 1678770178) return this.addXObj (val);
return this.addX (JS.SV.newV (10, JM.BondSet.newBS (val, this.vwr.ms.getAtomIndices (bs))));
}
return false;
}, "JS.T,JS.SV");
Clazz.defineMethod (c$, "getMathExt", 
 function () {
return (this.eval).getMathExt ();
});
Clazz.defineMethod (c$, "evalOp", 
function (token) {
if (!this.addOp (token) || !this.operate ()) return null;
return this.xStack[this.xPt--];
}, "JS.T");
Clazz.defineStatics (c$,
"qMods", " w:0 x:1 y:2 z:3 normal:4 eulerzxz:5 eulerzyz:6 vector:-1 theta:-2 axisx:-3 axisy:-4 axisz:-5 axisangle:-6 matrix:-9");
});
