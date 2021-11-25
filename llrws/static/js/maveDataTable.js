$(document).ready(function() {
	// Initialzie with empty data table.
	var table = $("#data").DataTable({
		// Disable initial sorting
		aaSorting: [],
		columns: [
			{data: "hgvs_pro", sortable: false},
			{data: "score", searchable: false},
			{data: "sd", searchable: false},
			{data: "se", searchable: false},
			{data: "llr",searchable: false},
			{data: "llrCIlower", searchable: false},
			{data: "llrCIupper", searchable: false},
		],
		language: {
			searchPlaceholder: "Search HGVS Pro",
		},
		lengthMenu: [
			[100, 250, 500, -1],
			[100, 250, 500, "All"],
		],
		pageLength: 100,
		scrollX: true,
		scrollY: "500px",
		scroller: true,
		scrollCollapse: true,
	});

	// Get table content on button click.
	$("#mave-button-submit").click(function() {
		$('#mave-button-submit').val('Loading...').prop('disabled', true);
		table.ajax.url("/data").load(function() {
			// Remove loaded Dropzone files on successful load.
			maveCSVDropzone = Dropzone.forElement("#mave-upload-csv");
    		maveCSVDropzone.removeAllFiles(true);
			// Reset text to default - 'Get MAVE'
			$('#mave-button-submit').val('Get MAVE').prop('disabled', true);
			// Scroll to bottom of page to show table
			$("html, body").animate({
				scrollTop: document.body.scrollHeight
			}, "slow");
		});
	});
});
