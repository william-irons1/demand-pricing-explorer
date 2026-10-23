"""Exercise the financial dashboard, completed findings and downloadable reports."""

import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from analysis import INVESTIGATION_LABELS, build_investigation, report_markdown


@pytest.fixture
def app():
    return AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'),
                             default_timeout=30).run()


def table_with(app, column):
    return next(element.value for element in app.dataframe if column in element.value.columns)


def test_benchmark_financial_metrics_and_complete_dashboard_are_displayed(app):
    assert not app.exception
    assert [m.value for m in app.metric if m.label == 'Optimal selling price'] == ['£10.50', '£12.00']
    assert [m.value for m in app.metric if m.label == 'Operating profit / week'] == ['£405.00', '£416.67']
    assert [m.value for m in app.metric if m.label == 'Revenue / week'] == ['£945.00', '£833.33']
    table = table_with(app, 'Maximum type')
    assert table['Quantity / week'].tolist() == pytest.approx([90, 625 / 9])
    assert table['Profit (£ / week)'].tolist() == pytest.approx([405, 1250 / 3])
    assert set(table_with(app, 'Check')['Check']) == {'Agrees with optimal set and value'}
    assert not app.text_area
    assert not app.text_input
    assert [tab.label for tab in app.tabs] == ['Pricing dashboard', 'Mathematics and verification',
                                               'Investigations and findings', 'Methodology and limitations']


def test_interface_contains_completed_analysis_without_unfinished_personal_prompts(app):
    assert not app.exception
    content = '\n'.join(element.value for element in app.markdown)
    for phrase in ('My prediction before opening the results', 'My reflection',
                   'To complete in your own words', 'Record your own reasoning',
                   'AI-assisted answers', 'Decisions and reasoning I personally contributed',
                   'This does not establish that you independently programmed the app'):
        assert phrase not in content
    assert not app.text_area
    assert not app.text_input
    assert 'Complete Mathematical Investigation and Findings' in [e.label for e in app.expander]
    assert any('AI assisted with code development and explanatory drafting' in e.value for e in app.caption)


@pytest.mark.parametrize('e', [0.5, 1.0])
def test_low_elasticity_is_supported_and_boundary_is_explicit(app, e):
    app.number_input('e').set_value(e).run()
    assert not app.exception
    assert not app.error
    table = table_with(app, 'Maximum type')
    ce = table[table['Demand model'] == 'Constant elasticity'].iloc[0]
    assert ce['Displayed price (£)'] == 15
    assert ce['Maximum type'] == 'Upper permitted boundary'
    assert any('upper permitted boundary' in warning.value for warning in app.warning)


def test_zero_cost_and_unit_elasticity_report_all_optimal_prices(app):
    app.number_input('e').set_value(1)
    app.number_input('c').set_value(0).run()
    assert not app.exception
    table = table_with(app, 'Maximum type')
    ce = table[table['Demand model'] == 'Constant elasticity'].iloc[0]
    assert ce['All optimal prices'] == '£1.00–£15.00'
    assert ce['Maximum type'] == 'Multiple equally optimal prices'
    assert ce['Profit (£ / week)'] == pytest.approx(1000)


def test_linear_plateau_reports_set_and_fixed_cost_loss(app):
    app.number_input('c').set_value(20)
    app.number_input('F').set_value(50)
    app.number_input('price_max').set_value(20).run()
    assert not app.exception
    row = table_with(app, 'Maximum type').iloc[0]
    assert row['All optimal prices'] == '£15.00–£20.00'
    assert row['Quantity / week'] == 0
    assert row['Profit (£ / week)'] == -50
    assert any('profit is −F' in warning.value for warning in app.warning)


@pytest.mark.parametrize('lower,upper', [(0, 15), (15, 15), (16, 15)])
def test_invalid_price_interval_stops_results(app, lower, upper):
    app.number_input('price_min').set_value(lower)
    app.number_input('price_max').set_value(upper).run()
    assert not app.exception
    assert app.error
    assert not app.metric
    assert not app.dataframe


def test_shared_lower_bound_and_infeasible_reference(app):
    app.number_input('price_min').set_value(12).run()
    assert not app.exception
    optimal = table_with(app, 'Maximum type')
    assert optimal['Displayed price (£)'].tolist() == [12, 12]
    assert set(optimal['Maximum type']) == {'Lower permitted boundary'}
    reference = table_with(app, 'Permitted price?')
    assert set(reference['Permitted price?']) == {'No: outside interval'}
    assert any('infeasible' in warning.value for warning in app.warning)


def test_graph_range_is_only_a_view_and_full_interval_is_available(app):
    maximum = next(w for w in app.number_input if w.label == 'Maximum displayed price (£)')
    maximum.set_value(9).run()
    assert not app.exception
    assert table_with(app, 'Maximum type')['Displayed price (£)'].tolist() == [10.5, 12]
    assert any('outside this graph view' in info.value for info in app.info)
    app.checkbox('full_view').check().run()
    graph = json.loads(app.get('plotly_chart')[0].proto.spec)
    assert graph['layout']['xaxis']['range'] == [1, 15]
    assert table_with(app, 'Maximum type')['Displayed price (£)'].tolist() == [10.5, 12]


def test_investigation_resets_every_other_assumption(app):
    app.number_input('c').set_value(7)
    app.number_input('F').set_value(80)
    app.number_input('price_max').set_value(11).run()
    app.selectbox('investigation').select(INVESTIGATION_LABELS['fixed_cost']).run()
    assert not app.exception
    table = table_with(app, 'Scenario')
    assert table['Displayed price (£)'].tolist() == [10.5, 12, 10.5, 12]
    assert table['Δ profit (£ / week)'].tolist() == pytest.approx([0, 0, -50, -50])
    assert [float(value) for value in table['Profit (£ / week)']] == pytest.approx([405, 1250 / 3, 355, 1100 / 3])


def test_loading_benchmark_restores_all_live_assumptions(app):
    for key, value in {'p0': 9, 'Q0': 120, 'c': 0, 'F': 50, 'e': 1, 'price_min': 3, 'price_max': 20}.items():
        app.number_input(key).set_value(value)
    app.selectbox('period').select('month').run()
    next(button for button in app.sidebar.button if button.label == 'Load benchmark').click().run()
    assert not app.exception
    for key, value in {'p0': 10, 'Q0': 100, 'c': 6, 'F': 0, 'e': 2, 'price_min': 1, 'price_max': 15}.items():
        assert app.number_input(key).value == value
    assert app.selectbox('period').value == 'week'


@pytest.mark.parametrize('key', ['elasticity', 'unit_cost', 'price_cap', 'fixed_cost', 'high_cost'])
def test_all_five_investigations_display_the_calculated_findings_and_financial_results(app, key):
    app.selectbox('investigation').select(INVESTIGATION_LABELS[key]).run()
    assert not app.exception
    item = build_investigation(key)
    table = table_with(app, 'Scenario')
    assert len(table) == len(item['rows'])
    for displayed, calculated in zip(table.to_dict('records'), item['rows']):
        assert displayed['Demand model'] == calculated['model_label']
        for column, field in [('Displayed price (£)', 'price'), ('Quantity / week', 'quantity'),
                              ('Revenue (£ / week)', 'revenue'), ('Profit (£ / week)', 'profit'),
                              ('Δ price (£)', 'price_change'), ('Δ profit (£ / week)', 'profit_change')]:
            assert displayed[column] == pytest.approx(calculated[field])
    content = '\n'.join(element.value for element in app.markdown)
    assert item['question'] in content
    assert item['theory'] in content
    assert item['interpretation'] in content
    assert item['financial_implications'] in content
    assert item['limitation'] in content
    assert item['conclusion'] in [element.value for element in app.success]
    assert not app.text_area


def test_revenue_and_profit_comparison_displays_different_prices_and_business_outcomes(app):
    assert not app.exception
    table = table_with(app, 'Objective')
    assert table['Objective'].tolist() == ['Maximum revenue', 'Maximum profit'] * 2
    assert table['Price (£)'].tolist() == pytest.approx([7.5, 10.5, 1, 12])
    assert table['Revenue (£ / week)'].tolist() == pytest.approx([1125, 945, 10000, 2500 / 3])
    assert table['Profit (£ / week)'].tolist() == pytest.approx([225, 405, -50000, 1250 / 3])


def test_revenue_numerical_range_error_preserves_available_profit_results(app):
    # CE profit near £6 remains representable, while revenue at £1 would require
    # about 1e402 units. A secondary objective must not crash the dashboard.
    app.number_input('e').set_value(400).run()
    assert not app.exception
    assert len(table_with(app, 'Maximum type')) == 2
    assert any('revenue' in element.value.lower() and
               ('range' in element.value.lower() or 'represent' in element.value.lower()
                or 'unavailable' in element.value.lower())
               for element in app.warning)


def test_revenue_view_and_period_labels_are_consistent(app):
    app.selectbox('period').select('month').run()
    app.radio('curve_view').set_value('Revenue').run()
    assert not app.exception
    assert 'Quantity / month' in table_with(app, 'Maximum type')
    graph = json.loads(app.get('plotly_chart')[0].proto.spec)
    assert graph['layout']['yaxis']['title']['text'] == 'Revenue (£ / month)'
    # The investigations are independent weekly benchmark experiments.
    assert 'Profit (£ / week)' in table_with(app, 'Scenario')


def test_exports_include_reproducible_financial_results_and_complete_model_generated_reports(monkeypatch):
    import csv
    import io
    import streamlit as st

    captured = {}
    original = st.download_button

    def capture(label, data, *args, **kwargs):
        captured[label] = data
        return original(label, data, *args, **kwargs)

    monkeypatch.setattr(st, 'download_button', capture)
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=30).run()
    assert not at.exception
    rows = list(csv.DictReader(io.StringIO(captured['Download results CSV'].decode('utf-8'))))
    assert len(rows) == 4
    assert {row['scenario'] for row in rows} == {'optimal', 'reference'}
    assert all(float(row['price_min']) == 1 and float(row['price_max']) == 15 for row in rows)
    assert all(row['period'] == 'week' for row in rows)
    optimal = [row for row in rows if row['scenario'] == 'optimal']
    assert [json.loads(row['optimal_intervals']) for row in optimal] == [[[10.5, 10.5]], [[12, 12]]]
    assert [float(row['profit']) for row in optimal] == pytest.approx([405, 1250 / 3])
    financial = list(csv.DictReader(io.StringIO(captured['Download financial comparison CSV'].decode('utf-8'))))
    assert len(financial) == 4
    assert [float(row['price']) for row in financial] == pytest.approx([7.5, 10.5, 1, 12])
    assert [float(row['profit']) for row in financial] == pytest.approx([225, 405, -50000, 1250 / 3])
    for row in financial:
        assert float(row['revenue']) - float(row['total_cost']) == pytest.approx(float(row['profit']))
        assert row['period'] == 'week'
        assert json.loads(row['optimal_intervals'])
    report = captured['Download complete findings report'].decode('utf-8')
    assert report == report_markdown()
    assert 'Complete Mathematical Investigation and Findings' in report
    assert 'AI-assisted answers' not in report
    assert 'Download my notes' not in captured
    assert 'Download completed worksheet' not in captured
    at.selectbox('investigation').select(INVESTIGATION_LABELS['unit_cost']).run()
    assert not at.exception
    assert captured['Download investigation report'].decode('utf-8') == report_markdown(['unit_cost'])
    investigation = list(csv.DictReader(io.StringIO(captured['Download investigation CSV'].decode('utf-8'))))
    assert len(investigation) == 4
    assert [float(row['c']) for row in investigation] == [6, 6, 7, 7]
    assert [float(row['price']) for row in investigation] == pytest.approx([10.5, 12, 11, 14])
    assert [float(row['profit']) for row in investigation] == pytest.approx([405, 1250 / 3, 320, 2500 / 7])
    at.selectbox('period').select('month').run()
    live_export = list(csv.DictReader(io.StringIO(captured['Download results CSV'].decode('utf-8'))))
    assert all(row['period'] == 'month' for row in live_export)
    assert captured['Download complete findings report'].decode('utf-8') == report


def test_chosen_price_comparison_and_graph_markers_follow_input(app):
    app.number_input('test_price').set_value(12).run()
    assert not app.exception
    tables = [e.value for e in app.dataframe if 'Financial measure' in e.value]
    assert len(tables) == 2
    for table, expected in zip(tables, [360, 1250 / 3]):
        row = table[table['Financial measure'] == 'Profit (£ / week)'].iloc[0]
        assert row['Chosen test price'] == f'{expected:,.2f}'
    graph = json.loads(app.get('plotly_chart')[0].proto.spec)
    chosen = [t for t in graph['data'] if 'at chosen price' in t.get('name', '')]
    assert len(chosen) == 2
    assert all(trace['x'] == [12] and trace['marker']['symbol'] == 'square' for trace in chosen)
    assert [trace['y'][0] for trace in chosen] == pytest.approx([360, 1250 / 3])
    risk = table_with(app, 'Lost profit (£ / week)')
    assert risk['Lost profit (£ / week)'].tolist() == pytest.approx([0, 1250/3 - 20000/49, 45, 0])


def test_chosen_price_is_kept_within_updated_interval_and_reset(app):
    app.number_input('test_price').set_value(14).run()
    app.number_input('price_max').set_value(11).run()
    assert not app.exception
    assert app.number_input('test_price').value == 11
    assert any('chosen price has been moved' in i.value for i in app.info)
    next(b for b in app.sidebar.button if b.label == 'Load benchmark').click().run()
    assert app.number_input('test_price').value == 10


def test_chosen_price_at_overflow_preserves_other_model_and_optimal_results(app):
    app.number_input('e').set_value(400).run()
    app.number_input('test_price').set_value(1).run()
    assert not app.exception
    assert len(table_with(app, 'Maximum type')) == 2
    assert any('Chosen-price comparison unavailable for Constant elasticity' in w.value for w in app.warning)
    tables = [e.value for e in app.dataframe if 'Financial measure' in e.value]
    assert len(tables) == 1


def test_new_comparison_downloads_preserve_inputs_precision_sets_and_period(monkeypatch):
    import csv
    import io
    import streamlit as st
    from analysis import summary_markdown

    captured = {}
    original = st.download_button

    def capture(label, data, *args, **kwargs):
        captured[label] = data
        return original(label, data, *args, **kwargs)

    monkeypatch.setattr(st, 'download_button', capture)
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=30).run()
    at.number_input('test_price').set_value(12).run()
    assert not at.exception
    chosen = list(csv.DictReader(io.StringIO(captured['Download chosen-price comparison CSV'].decode())))
    risk = list(csv.DictReader(io.StringIO(captured['Download model-risk comparison CSV'].decode())))
    assert len(chosen) == 6 and len(risk) == 4
    assert float(chosen[4]['profit']) == pytest.approx(1250/3, rel=1e-14)
    assert float(risk[1]['regret']) == pytest.approx(1250/3 - 20000/49, rel=1e-13)
    assert all(float(r['price_min']) == 1 and float(r['price_max']) == 15 for r in chosen + risk)
    assert all(r['period'] == 'week' for r in chosen + risk)
    assert all(json.loads(r['optimal_intervals']) for r in chosen)
    assert all(json.loads(r['candidate_optimal_intervals']) for r in risk)
    assert captured['Download concise findings summary'].decode() == summary_markdown()
    at.number_input('c').set_value(20)
    at.number_input('F').set_value(50)
    at.number_input('price_max').set_value(20).run()
    chosen = list(csv.DictReader(io.StringIO(captured['Download chosen-price comparison CSV'].decode())))
    assert all(r['profit_change_percent'] == '' for r in chosen)
    risk = list(csv.DictReader(io.StringIO(captured['Download model-risk comparison CSV'].decode())))
    assert json.loads(risk[0]['candidate_optimal_intervals']) == [[15,20]]
    at.selectbox('period').select('month').run()
    risk = list(csv.DictReader(io.StringIO(captured['Download model-risk comparison CSV'].decode())))
    assert all(r['period'] == 'month' for r in risk)


def test_large_fixed_cost_preserves_meaningful_displayed_differences(app):
    app.number_input('F').set_value(1e20).run()
    assert not app.exception
    profits = [m for m in app.metric if m.label == 'Operating profit / week']
    assert profits[0].delta == '£+5.00 vs starting price'
    assert profits[1].delta == '£+16.67 vs starting price'
    assert any('maximum profit by £11.67/week' in i.value for i in app.info)
    assert any('£180.00 more profit/week' in m.value for m in app.markdown)
