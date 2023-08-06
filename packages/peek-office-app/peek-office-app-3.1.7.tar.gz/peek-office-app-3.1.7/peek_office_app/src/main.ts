import { platformBrowserDynamic } from "@angular/platform-browser-dynamic"
import { enableProdMode } from "@angular/core"
import { environment } from "./environments/environment"
import { VortexService } from "@synerty/vortexjs"
import { AppModule } from "./app/app.module"

const protocol = location.protocol.toLowerCase() === "https:" ? "wss" : "ws"

VortexService.setVortexUrl(`${protocol}://${location.hostname}:${location.port}/vortexws`)
VortexService.setVortexClientName("peek-office-app")

if (environment.production) {
    enableProdMode()
}

platformBrowserDynamic()
    .bootstrapModule(AppModule)
