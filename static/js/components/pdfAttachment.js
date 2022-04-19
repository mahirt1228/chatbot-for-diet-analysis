/**
 * renders pdf attachment on to the chat screen
 * @param {Object} pdf_data json object
 */
function openPdf(pdf_url) {
    window.open(pdf_url, '_blank');
}

function renderPdfAttachment(pdf_data) {
    const { url: pdf_url } = pdf_data.custom;
    const { title: pdf_title } = pdf_data.custom;
    const pdf_attachment = `<a href="#" onClick="window.open('${pdf_url}', '_blank',
    'fullscreen=yes'); return false;"><div class="pdf_attachment"><div class="row"><div class="col-xs-2 pdf_icon">
<i class="fa fa-file-pdf-o" aria-hidden="true" style="font-size:20px;"></i>${` `+ pdf_title}</div><div class="col-xs-2" style="color:black;" pdf_link"></a>
 </div></div></div><div class="clearfix"></div>
 <img class="botAvatar" src="./static/img/sara_avatar.png" >
 <p class="botMsg" >Do you want to Chat again?</p>
 <div class="clearfix" ></div>`;
    
    // console.log(pdf_url);

    $(".chats").append(pdf_attachment);
    scrollToBottomOfResults();
}

