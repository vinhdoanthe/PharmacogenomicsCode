$(document).ready(function () {
    let structures_scrollable = $("#structures_scrollable")
    structures_scrollable.show();
    let oTable1 = structures_scrollable.DataTable({
        deferRender: true,
        scrollY: true,
        scrollX: true,
        scrollCollapse: true,
        scroller: true,
        paging: true,
        bSortCellsTop: false, //prevent sort arrows going on bottom row
        aaSorting: [],
        autoWidth: true,
        bInfo: true,
        //order: [[7, "asc"]],
        pagingType: 'full_numbers',
        lengthMenu: [
            [10, 25, 50, 100, 200, -1],
            [10, 25, 50, 100, 200, 'All'],
        ],
    })

    oTable1.on('draw.dt', function () {

    });

    let column_filters = [];

    // Variant
    column_filters = column_filters.concat(createYADCFfilters(0, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Transcript
    column_filters = column_filters.concat(createYADCFfilters(1, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // cDNA_position
    column_filters = column_filters.concat(createYADCFfilters(2, 1, "multi_select", "select2", 'Select', false, null, null, "80px"));

    // CDS_position
    column_filters = column_filters.concat(createYADCFfilters(3, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Protein_position
    column_filters = column_filters.concat(createYADCFfilters(4, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Amino_acids
    column_filters = column_filters.concat(createYADCFfilters(5, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Codons
    column_filters = column_filters.concat(createYADCFfilters(6, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Consequence
    column_filters = column_filters.concat(createYADCFfilters(8, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // Impact
    column_filters = column_filters.concat(createYADCFfilters(9, 1, "multi_select", "select2", "Select", false, null, null, "80px"));

    // BayesDel_addAF_rankscore
    column_filters = column_filters.concat(createYADCFfilters(10, 40, "range_number", null, ["Min", "Max"], false, null, null, "40px"))

    yadcf.init(oTable1.draw(), column_filters, {
        cumulative_filtering: false
    });

    //yadcf.exFilterColumn(oTable1, [[8, ["mis"]]], true);

    gray_scale_table(structures_scrollable);
    $("#reset").click(function () {
        yadcf.exResetAllFilters(oTable1);
    });
});
