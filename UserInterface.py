
    # HTML for 2D fitter form
htmlForm_2D = '''
<table border=1 cellpadding=20>
<tr><td><b>Example 2D f(x) Web Fitter</b></td></tr>
<tr><td>
<form action="/simplefitter_2D" method="post" target=_blank>
--- 2D Text Data ---<br>
<textarea  rows="10" cols="45" name="textdata" wrap=off>
Example 2D data for testing
  X        Y
5.357    10.376
5.457    10.489
5.936    11.049
6.161    11.327 ending text is ignored
6.697    12.054
8.442    14.744
9.769    17.068
9.861    17.104

</textarea>
<br><br>
    --- Example 2D Equations ---<br>
<input type="radio" name="equation" value="Linear" checked>Linear Polynomial<br>
<input type="radio" name="equation" value="Quadratic">Quadratic Polynomial<br>
<input type="radio" name="equation" value="Cubic">Cubic Polynomial<br>
<input type="radio" name="equation" value="WitchA">Witch Of Maria Agnesi A<br>
<input type="radio" name="equation" value="LorentzianPeakCWithOffset">Lorentzian Peak C With Offset<br>
<input type="radio" name="equation" value="GammaRayDegreesB">Gamma Ray Angular Distribution (degrees) B<br>
<input type="radio" name="equation" value="ExponentialWithOffset">Exponential With Offset<br>
<br>
<table><tr>
<td>
<input type="submit" value="Submit">
</td>
<td align="left">
<input type="radio" name="target" value="SSQABS" checked>Lowest Sum Of Squared Absolute Error<br>
<input type="radio" name="target" value="LNQREL">Lowest Sum Of Squared Log[Pred/Actual]<br>
<input type="radio" name="target" value="SSQREL">Lowest Sum Of Squared Relative Error<br>
<input type="radio" name="target" value="ODR">Lowest Sum Of Squared Orthogonal Distance<br>
</td>
</tr></table>
</form>
<br><br>
<a href="/equationlist_2D">Link to all standard 2D equations</a>
</td></tr></table>
'''



    # HTML for 3D fitter form
htmlForm_3D = '''
<table border=1 cellpadding=20>
<tr><td><b>Example 3D f(x,y) Web Fitter</b></td></tr>
<tr><td>
<form action="/simplefitter_3D" method="post" target=_blank>
--- 3D Text Data ---<br>
<textarea  rows="10" cols="45" name="textdata" wrap=off>
Example 3D data for testing
    X      Y       Z
  3.017  2.175   0.0320
  2.822  2.624   0.0629
  1.784  3.144   6.570
  1.712  3.153   6.721
  2.972  2.106   0.0313
  2.719  2.542   0.0643
  2.0 2.6 4.0  ending text is ignored
  1.479  2.957   6.583
  1.387  2.963   6.744
  2.843  1.984   0.0315
  2.485  2.320   0.0639
  0.742  2.568   6.581
  0.607  2.571   6.753
</textarea>
<br><br>
    --- Example 3D Equations ---<br>
<input type="radio" name="equation" value="Linear" checked>Linear Polynomial<br>
<input type="radio" name="equation" value="FullQuadratic">Full Quadratic Polynomial<br>
<input type="radio" name="equation" value="FullCubic">Full Cubic Polynomial<br>
<input type="radio" name="equation" value="MonkeySaddleA">Monkey Saddle A<br>
<input type="radio" name="equation" value="GaussianCurvatureOfWhitneysUmbrellaA">Gaussian Curvature Of Whitneys Umbrella A<br>
<input type="radio" name="equation" value="NIST_NelsonAutolog">NIST Nelson Autolog<br>
<input type="radio" name="equation" value="CustomPolynomialOne">Custom Polynomial One<br>
<br>

<table><tr>
<td>
<input type="submit" value="Submit">
</td>
<td align="left">
<input type="radio" name="target" value="SSQABS" checked>Lowest Sum Of Squared Absolute Error<br>
<input type="radio" name="target" value="LNQREL">Lowest Sum Of Squared Log[Pred/Actual]<br>
<input type="radio" name="target" value="SSQREL">Lowest Sum Of Squared Relative Error<br>
<input type="radio" name="target" value="ODR">Lowest Sum Of Squared Orthogonal Distance<br>
</td>
</tr></table>
</form>

<br><br>

<a href="/equationlist_3D">Link to all standard 3D equations</a>
</td></tr></table>
'''
