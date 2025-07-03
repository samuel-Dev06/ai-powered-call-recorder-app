import { Component } from '@angular/core';
import {MatCardModule} from "@angular/material/card";
import {MatChipsModule} from "@angular/material/chips";
import {TablerIconsModule} from "angular-tabler-icons";
import {MatButtonModule} from "@angular/material/button";

@Component({
  selector: 'app-upload-call',
  imports: [MatCardModule, MatChipsModule, TablerIconsModule, MatButtonModule],
  templateUrl: './upload-call.component.html',
  styleUrl: './upload-call.component.scss'
})
export class UploadCallComponent {

}
