// var customBarColors = {
//   success: '#28a745',
//   error: '#dc3545',
//   ignored: '#7a7a7a',
//   progress: '#007bff',
// }

// function customProgress(progressBarElement, progressBarMessageElement, progress) {
//   if (progress.current == 0) {
//     if (progress.pending === true) {
//       progressBarMessageElement.textContent = 'Waiting for task to start...';
//     } else {
//       progressBarMessageElement.textContent = 'Task started...';
//     }
//   } else {
//     progressBarMessageElement.textContent = progress.description;
//   }
//   progressBarElement.style.width = String(progress.percent) + "%";
//   progressBarElement.style.background = this.barColors.progress;
// }

// function customSuccess(progressBarElement, progressBarMessageElement) {
//   progressBarElement.style.background = this.barColors.success;
//   progressBarMessageElement.innerHTML = 'Analysis Completed!';
// }

// function customError(progressBarElement, progressBarMessageElement) {
//   progressBarElement.style.background = this.barColors.error;
//   progressBarMessageElement.innerHTML = 'Something Went Wrong!';
// }

// function customResult(resultElement, result) {
//   let rb = result[1];
//   if (rb == 0) {
//     // this means analysis is not successfull,i.e. some error occured
//     resultElement.innerHTML = "<p>" + result[0] + "</p>";
//   }
//   else if ((rb == 1) && (result.length == 2))
//   {
//     // this means analysis is successfull & it's of a single link
//     let pdf_report = result[0];
//     var url = 'media/' + pdf_report;
//     resultElement.innerHTML = "<p>Click <a href =" + url + " download >Here</a> to download report</p>";
//   }

//   if (result.length == 3) {
//     // this means it was a file
//     resultElement.innerHTML = result[0] + result[2];
//   }
// }

// function check_link() {
//   var link_element = document.getElementsByName('link')[0];
//   var link = link_element.value;
//   var modal_text = document.getElementById('modal_text');
//   console.log(link);

//   if (link.length === 0) {
//     modal_text.innerHTML = "Enter a Link!";
//     link_element.click();
//     link_element.value = "";
//     return false;
//   } else {
//     // Validate The Link
//     modal_text.innerHTML = "Wait while we process the link ...";
//     document.getElementsByName('link_form')[0].submit();
//     link_element.click();
//     return true;
//   }
// }
