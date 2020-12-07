import json

import numpy as np

from bokeh import events
from bokeh.layouts import row, column
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import CustomJS,Slider, Grid, LinearAxis, MultiLine, Patches, CheckboxButtonGroup,HoverTool, Button
from bokeh.embed import json_item, file_html
from bokeh.resources import CDN
from scipy import signal

from bokeh_fc.libs.SegRead.Seg import  SegReader

start_const_gain=1e3
invert=0
detrend=0
dt=0.001
my_stupid_gain=1
NUM = 30
comment='Test Seismogramm'
wiggle=1
Some_line=0
noise=False
n_level=0.1
figsize=(40,15)
font=25
grid=True
clipping=True
wiggle=True

file1='bokeh_fc/240_cut_edited.segy'


wind_dowm,wind_up=500,0
class TestBokeh():

    def __init__(self):
        pass

    def insert_zeros_in_trace(self,trace):
        time = np.arange(len(trace))
        zero_idx = np.where(np.diff(np.signbit(trace)))[0]

        time_at_zero = time[zero_idx] - trace[zero_idx] / np.diff(trace)[zero_idx]
        trace_z = np.insert(trace, zero_idx + 1, 0)
        time_z = np.insert(time, zero_idx + 1, time_at_zero)
        return trace_z, time_z

    def add_tags_for_varea(self,trace, time, level):
        trace_tagged = np.insert(trace, 0, 0)
        trace_tagged = np.insert(trace_tagged, len(trace_tagged), level)
        time_tagged = np.linspace(time[0], time[-1], len(trace_tagged))

        return trace_tagged, time_tagged

    def display_event(self, attributes=[]):
        """
        Function to build a suitable CustomJS to display the current event
        in the div model.
        """
        style = 'float: left; clear: left; font-size: 13px'
        return CustomJS( code="""
            var attrs = %s;
            var args = [];
            for (var i = 0; i < attrs.length; i++) {
                var val = JSON.stringify(cb_obj[attrs[i]], function(key, val) {
                    return val.toFixed ? Number(val.toFixed(2)) : val;
                })
                args.push(attrs[i] + '=' + val)
            }
            var line = "<span style=%r><b>" + cb_obj.event_name + "</b>(" + args.join(", ") + ")</span>\\n";
            var text = div.text.concat(line);
            var lines = text.split("\\n")
            if (lines.length > 35)
                lines.shift();
            div.text = lines.join("\\n");
        """ % (attributes, style))
    def main(self):
        print("startb2")
        S = SegReader()
        S.open(file1)
        Traces, bin_head, trace_head = S.read_all()
        length = np.arange(0, len(Traces[0]))
        offsets = trace_head['offset']
        step = (abs(offsets[len(offsets) - 1]) + abs(offsets[0])) / (len(offsets) - 1)
        first_sou = 0
        last_sou = len(Traces) * step
        Num_of_traces = len(Traces)
        stoffset = {i: i * step for i in range(Num_of_traces)}
        clip = step - 0.1

        #  if clipping==True:
        #    Traces_step1[Traces_step1 > clip] = clip
        #  Traces_step1[Traces_step1 < -clip] = -clip

        Traces_final = np.zeros((len(Traces), len(Traces[0][wind_up:wind_dowm])))
        for i in range(0, Num_of_traces):
            Traces_final[i] = Traces[i][wind_up:wind_dowm]
        if detrend == 1:
            Traces_final = signal.detrend(Traces_final)

        Vareas_mass = []
        Trace_mass = []
        Time_mass = []
        for k in range(Num_of_traces):
            Traces = Traces_final[k] * step / np.max(Traces_final[k])
            Vareas = np.where(Traces > 0, Traces, 0)
            Traces_step1, Time_step1 = self.insert_zeros_in_trace(Traces)

            Traces_step11 = Traces_step1
            Traces_step11[-1] = 0
            Traces_step11[0] = 0

            a = np.where(Traces_step11 > 0, Traces_step11, 0)

            Trace_mass.append(Traces_step11)
            Vareas_mass.append(a)
            Time_mass.append(Time_step1)
            ###############################################################################
        source_L = ColumnDataSource(dict(
            xs=[Trace_mass[i] + step * i for i in range(Num_of_traces)],
            ys=[Time_mass[i] for i in range(Num_of_traces)]

        )
        )
        source_copy_L = ColumnDataSource(dict(
            xs=[Trace_mass[i] + step * i for i in range(Num_of_traces)],
            ys=[Time_mass[i] for i in range(Num_of_traces)]

        )
        )

        source_P = ColumnDataSource(dict(
            xs=[Vareas_mass[i] + step * i for i in range(Num_of_traces)],
            ys=[Time_mass[i] for i in range(Num_of_traces)]
        )
        )
        source_copy_P = ColumnDataSource(dict(
            xs=[Vareas_mass[i] + step * i for i in range(Num_of_traces)],
            ys=[Time_mass[i] for i in range(Num_of_traces)]
        )
        )

        ###############################################################################


        plot = figure(title=comment, plot_width=1600, plot_height=800, x_range=(first_sou - 5, last_sou + 5))

        gain_slider = Slider(start=-99., end=100., value=1., step=0.01, title="Gain", default_size=(50))
        checkbox_button_group = CheckboxButtonGroup(labels=["Wiggle", "Clipping"], active=[0, 0, 0], default_size=(50))

        glyph_L = MultiLine(xs="xs", ys="ys", line_color="#8073ac", line_width=2)
        L = plot.add_glyph(source_L, glyph_L)
        hover = HoverTool(tooltips=[('xs', '@xs'), ('ys', '@ys')])

        glyph_P = Patches(xs="xs", ys="ys", fill_color="#fb9a99", line_alpha=0.1)
        P = plot.add_glyph(source_P, glyph_P)

        # x_l=np.arange(first_sou,last_sou,step)


        callback = CustomJS(args=dict(c=step, source_L=source_L, source_copy_L=source_copy_L, source_P=source_P,
                                      source_copy_P=source_copy_P, gain=gain_slider,
                                      checkbox_button_group=checkbox_button_group),
                            code="""
                var clip = c-0.1;
                var paint = !!checkbox_button_group.active.includes(0);
                console.log(paint)
                var clipping = !!checkbox_button_group.active.includes(1);
                console.log(clipping)
                var data_L = source_L.data;
                var data_copy_L = source_copy_L.data;
                var data_P = source_P.data;
                var data_copy_P = source_copy_P.data;

                var G = gain.value;

                for (var i = 0; i <  data_L['xs'].length; i++) {
                    var Trace_mass_copy_L = data_copy_L['xs'][i]
                    var Vareas_mass_copy_P = data_copy_P['xs'][i]
                    var Trace_mass_L = data_L['xs'][i]
                    var Vareas_mass_P = data_P['xs'][i]

                    if (paint && clipping || clipping && paint){
                        for (var j = 0; j <  Trace_mass_L.length; j++) {
                            Trace_mass_L[j]=((Trace_mass_copy_L[j]-c*i)*G);
                            Vareas_mass_P[j]=((Vareas_mass_copy_P[j]-c*i)*G);
                            if(Trace_mass_L[j]>=clip){
                                Trace_mass_L[j]=clip;
                            }
                            else if(Trace_mass_L[j]<-clip){
                                Trace_mass_L[j]=-clip;
                            }
                            if(Vareas_mass_P[j]>=clip){
                                Vareas_mass_P[j]=clip;
                            }
                            else if(Vareas_mass_P[j]<-clip){
                                Vareas_mass_P[j]=-clip;
                            }
                            Trace_mass_L[j]=Trace_mass_L[j]+c*i;
                            Vareas_mass_P[j]=Vareas_mass_P[j]+c*i;  
                        }

                    }

                    if (paint && !clipping || !clipping && paint){
                        for (var j = 0; j <  Trace_mass_L.length; j++) {
                            Trace_mass_L[j]=((Trace_mass_copy_L[j]-c*i)*G);
                            Vareas_mass_P[j]=((Vareas_mass_copy_P[j]-c*i)*G);
                            Trace_mass_L[j]=Trace_mass_L[j]+c*i;
                            Vareas_mass_P[j]=Vareas_mass_P[j]+c*i; 
                        }        
                    }        
                    if (!paint && clipping || clipping && !paint){
                        for (var j = 0; j <  Trace_mass_L.length; j++){
                            Trace_mass_L[j]=((Trace_mass_copy_L[j]-c*i)*G);
                            Vareas_mass_P[j] = 0+c*i;
                            if(Trace_mass_L[j]>=clip){
                                Trace_mass_L[j]=clip;
                            }
                            if(Trace_mass_L[j]<-clip){
                                Trace_mass_L[j]=-clip;
                            }
                            Trace_mass_L[j]=Trace_mass_L[j]+c*i;
                        }

                    }
                    if (!paint && !clipping || !clipping && !paint){
                        for (var j = 0; j <  Trace_mass_L.length; j++) {
                            Trace_mass_L[j]=((Trace_mass_copy_L[j]-c*i)*G);
                            Vareas_mass_P[j] = 0+c*i;
                            Trace_mass_L[j]=Trace_mass_L[j]+c*i;
                    }        
                    }     
                }
                source_L.change.emit();
                source_P.change.emit();
            """)

        button = Button(label="Button", button_type="success", width=300)
        point_attributes = ['x', 'y']

        checkbox_button_group.js_on_click(callback)
        gain_slider.js_on_change('value', callback)

        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'above')

        yaxis = LinearAxis()
        plot.add_layout(yaxis, 'right')

        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

        layout1 = row(
            column(plot, gain_slider, checkbox_button_group),

        )
        # curdoc().add_root(plot)
        plot.y_range.flipped = True

        # plot.add_tools(hover)
        layout1 = column( gain_slider, checkbox_button_group,plot,)
                #return json.dumps(json_item(plot,"myplot"))

        return file_html(layout1, CDN, "my plot")
