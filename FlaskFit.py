import os, sys, inspect

import pyeq3, GraphUtils, TextUtils, UserInterface, FileInfo
from flask import Flask
from flask import request


# override Flask's default file cache for the files we generate
class MyFlask(Flask):
    def get_send_file_max_age(self, name):
        if name.lower().endswith('.png'):
            return 0.000001
        if name.lower().endswith('.txt'):
            return 0.000001
        if name.lower().endswith('.html'):
            return 0.000001
        return Flask.get_send_file_max_age(self, name)


app = MyFlask(__name__)
app.debug = True # only for development, never for production


@app.route('/')
def UserInterfaceHTML():
    # return HTML to Flask as a web page
    s = '<html><body>'
    s += '<table><tr>'
    s += '<td>' + UserInterface.htmlForm_2D + '</td>'
    s += '<td> </td>'
    s += '<td>' + UserInterface.htmlForm_3D + '</td>'
    s += '</tr></table>'
    s +='</body></html>'

    return s


@app.route('/simplefitter_2D', methods=['POST'])
def simplefitter_2D_NoFormDataValidation():
    formTextData = request.form['textdata']
    formEquation = request.form['equation']
    formFittingTarget = request.form['target']

    if formEquation == 'Linear':
        equation = pyeq3.Models_2D.Polynomial.Linear(formFittingTarget)
    elif formEquation == 'Quadratic':
        equation = pyeq3.Models_2D.Polynomial.Quadratic(formFittingTarget)
    elif formEquation == 'Cubic':
        equation = pyeq3.Models_2D.Polynomial.Cubic(formFittingTarget)
    elif formEquation == 'WitchA':
        equation = pyeq3.Models_2D.Miscellaneous.WitchOfAgnesiA(formFittingTarget)
    elif formEquation == 'LorentzianPeakCWithOffset':
        equation = pyeq3.Models_2D.Peak.LorentzianPeakC(formFittingTarget, 'Offset')
    elif formEquation == 'GammaRayDegreesB':
        equation = pyeq3.Models_2D.LegendrePolynomial.GammaRayAngularDistributionDegreesB(formFittingTarget)
    elif formEquation == 'ExponentialWithOffset':
        equation = pyeq3.Models_2D.Exponential.Exponential(formFittingTarget, 'Offset')

    # the name of the data here is from the form
    # check for functions requiring non-zero nor non-negative data such as 1/x, etc.
    try:
        pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(formTextData, equation, False)
    except:
        return equation.reasonWhyDataRejected

    # check for number of coefficients > number of data points to be fitted
    coeffCount = len(equation.GetCoefficientDesignators())
    dataCount = len(equation.dataCache.allDataCacheDictionary['DependentData'])
    if coeffCount > dataCount:
        return "This equation requires a minimum of " + repr(coeffCount) + " data points, you supplied " + repr(dataCount) + "."

    equation.Solve()
    equation.CalculateModelErrors(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.CalculateCoefficientAndFitStatistics()

    # save fit statistics to a text file
    TextUtils.SaveCoefficientAndFitStatistics(FileInfo.fitStatisticsFilePath_2D,  equation)

    # save source code to a single text file, all available languages
    TextUtils.SaveSourceCode(FileInfo.sourceCodeFilePath_2D,  equation)

    # create graph
    title = "Model with 95% Confidence Intervals"
    xAxisLabel = "X data"
    yAxisLabel = "Y data"
    GraphUtils.SaveModelScatterConfidence(FileInfo.modelPlotFilePath_2D,
                                          equation, title, xAxisLabel, yAxisLabel) 

    title = "Absolute Error"
    GraphUtils.SaveAbsErrorScatterPlot(FileInfo.absErrorPlotFilePath_2D, equation, title, yAxisLabel)
    
    title = "Absolute Error"
    GraphUtils.SaveDataHistogram(FileInfo.absErrorHistFilePath_2D, equation.modelAbsoluteError, title)
    
    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        title = "Percent Error"
        GraphUtils.SavePercentErrorScatterPlot(FileInfo.perErrorPlotFilePath_2D, equation, title, yAxisLabel)
        
        title = "Percent Error"
        GraphUtils.SaveDataHistogram(FileInfo.perErrorHistFilePath_2D, equation.modelPercentError, title)


    # generate HTML
    htmlToReturn = ''
    htmlToReturn +=  equation.GetDisplayName() + '<br><br>\n'
    htmlToReturn +=  equation.GetDisplayHTML() + '<br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.fitStatisticsURL_2D + '">Link to parameter and fit statistics</a><br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.sourceCodeURL_2D + '">Link to source code, all available languages</a><br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.additionalInfoURL + '">Link to additional information</a><br><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.modelPlotURL_2D + '"> <br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.absErrorPlotURL_2D + '"><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.absErrorHistURL_2D + '"><br>\n'
    
    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        htmlToReturn +=  '<img src="' + FileInfo.perErrorPlotURL_2D + '"><br><br>\n'
        htmlToReturn +=  '<img src="' + FileInfo.perErrorHistURL_2D + '"><br><br>\n'

    return '<html><body>' + htmlToReturn + '</body></html>'


@app.route('/simplefitter_3D', methods=['POST'])
def simplefitter_3D_NoFormDataValidation():
    
    formTextData = request.form['textdata']
    formEquation = request.form['equation']
    formFittingTarget = request.form['target']

    if formEquation == 'Linear':
        equation = pyeq3.Models_3D.Polynomial.Linear(formFittingTarget)
    elif formEquation == 'FullQuadratic':
        equation = pyeq3.Models_3D.Polynomial.FullQuadratic(formFittingTarget)
    elif formEquation == 'FullCubic':
        equation = pyeq3.Models_3D.Polynomial.FullCubic(formFittingTarget)
    elif formEquation == 'MonkeySaddleA':
        equation = pyeq3.Models_3D.Miscellaneous.MonkeySaddleA(formFittingTarget)
    elif formEquation == 'GaussianCurvatureOfWhitneysUmbrellaA':
        equation = pyeq3.Models_3D.Miscellaneous.GaussianCurvatureOfWhitneysUmbrellaA(formFittingTarget)
    elif formEquation == 'NIST_NelsonAutolog':
        equation = pyeq3.Models_3D.NIST.NIST_NelsonAutolog(formFittingTarget)
    elif formEquation == 'CustomPolynomialOne': # X order 3, Y order 1 in this example - passed as integers
        equation = pyeq3.Models_3D.Polynomial.UserSelectablePolynomial(formFittingTarget, "Default", 3, 1)
    
    # the name of the data here is from the form
    # check for functions requiring non-zero nor non-negative data such as 1/x, etc.
    try:
        pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(formTextData, equation, False)
    except:
        return equation.reasonWhyDataRejected

    # check for number of coefficients > number of data points to be fitted
    coeffCount = len(equation.GetCoefficientDesignators())
    dataCount = len(equation.dataCache.allDataCacheDictionary['DependentData'])
    if coeffCount > dataCount:
        return "This equation requires a minimum of " + repr(coeffCount) + " data points, you supplied " + repr(dataCount) + "."

    equation.Solve()
    equation.CalculateModelErrors(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
    equation.CalculateCoefficientAndFitStatistics()

    # save fit statistics to a text file
    TextUtils.SaveCoefficientAndFitStatistics(FileInfo.fitStatisticsFilePath_3D,  equation)

    # save source code to a single text file, all available languages
    TextUtils.SaveSourceCode(FileInfo.sourceCodeFilePath_3D,  equation)

    # create graphs
    surfaceTitle = "Surface Plot"
    contourTitle = "Contour Plot"
    xAxisLabel = "X data"
    yAxisLabel = "Y data"
    zAxisLabel = "Z data"
    GraphUtils.SurfaceAndContourPlots(FileInfo.modelPlotFilePath_3D,
                                      FileInfo.contourPlotFilePath_3D,
                                      equation, surfaceTitle, contourTitle,
                                      xAxisLabel, yAxisLabel, zAxisLabel)

    title = "Absolute Error"
    GraphUtils.SaveAbsErrorScatterPlot(FileInfo.absErrorPlotFilePath_3D, equation, title, zAxisLabel)

    title = "Absolute Error"    
    GraphUtils.SaveDataHistogram(FileInfo.absErrorHistFilePath_3D, equation.modelAbsoluteError, title)

    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        title = "Percent Error"
        GraphUtils.SavePercentErrorScatterPlot(FileInfo.perErrorPlotFilePath_3D, equation, title, zAxisLabel)
        
        title = "Percent Error"
        GraphUtils.SaveDataHistogram(FileInfo.perErrorHistFilePath_3D, equation.modelPercentError, title)

    # generate HTML
    htmlToReturn = ''
    htmlToReturn +=  equation.GetDisplayName() + '<br><br>\n'
    htmlToReturn +=  equation.GetDisplayHTML() + '<br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.fitStatisticsURL_3D + '">Link to parameter and fit statistics</a><br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.sourceCodeURL_3D + '">Link to source code, all available languages</a><br><br>\n'
    htmlToReturn += '<a href="' + FileInfo.additionalInfoURL + '">Link to additional information</a><br><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.modelPlotURL_3D + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.contourPlotURL_3D + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.absErrorPlotURL_3D + '"><br><br>\n'
    htmlToReturn +=  '<img src="' + FileInfo.absErrorHistURL_3D + '"><br><br>\n'
    if equation.dataCache.DependentDataContainsZeroFlag != 1:
        htmlToReturn +=  '<img src="' + FileInfo.perErrorPlotURL_3D + '"><br><br>\n'
        htmlToReturn +=  '<img src="' + FileInfo.perErrorHistURL_3D + '"><br><br>\n'

    return '<html><body>' + htmlToReturn + '</body></html>'


@app.route('/equationlist_2D', methods=['GET'])
def equationlist_2D():
    htmlToReturn = '' # build this as we progress

    htmlToReturn += '<table border=1>'
    
    for submodule in inspect.getmembers(pyeq3.Models_2D):
        if inspect.ismodule(submodule[1]):
            for equationClass in inspect.getmembers(submodule[1]):
                if inspect.isclass(equationClass[1]):
                    for extendedVersionName in ['Default', 'Offset']:
                        if (-1 != extendedVersionName.find('Offset')) and (equationClass[1].autoGenerateOffsetForm == False):
                            continue
    
                        equation = equationClass[1]('SSQABS', extendedVersionName)
                        htmlToReturn += '<tr>'
                        htmlToReturn += '<td nowrap><b>2D ' + submodule[0] + '</b></td>'
                        htmlToReturn += '<td nowrap><i>' + equation.GetDisplayName() + '</i></td>'
                        htmlToReturn += '<td nowrap>' + equation.GetDisplayHTML() + '</td>'
                        htmlToReturn += '</tr>'
                        
    htmlToReturn += '</table>'
                        
    return '<html><body>' + htmlToReturn + '</body></html>'


@app.route('/equationlist_3D', methods=['GET'])
def equationlist_3D():
    htmlToReturn = '' # build this as we progress
    
    htmlToReturn += '<table border=1>'
    
    for submodule in inspect.getmembers(pyeq3.Models_3D):
        if inspect.ismodule(submodule[1]):
            for equationClass in inspect.getmembers(submodule[1]):
                if inspect.isclass(equationClass[1]):
                    for extendedVersionName in ['Default', 'Offset']:
                        if (-1 != extendedVersionName.find('Offset')) and (equationClass[1].autoGenerateOffsetForm == False):
                            continue
    
                        equation = equationClass[1]('SSQABS', extendedVersionName)
                        htmlToReturn += '<tr>'
                        htmlToReturn += '<td nowrap><b>3D ' + submodule[0] + '</b></td>'
                        htmlToReturn += '<td nowrap><i>' + equation.GetDisplayName() + '</i></td>'
                        htmlToReturn += '<td nowrap>' + equation.GetDisplayHTML() + '</td>'
                        htmlToReturn += '</tr>'
                        
    htmlToReturn += '</table>'

    return '<html><body>' + htmlToReturn + '</body></html>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
