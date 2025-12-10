import { Button, Modal } from "@grafana/ui";
import { useState } from "react";

export default function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [inputValue, setInputValue] = useState("");

  return (
    <>
      <div>
        <Button onClick={() => setIsModalOpen(true)}>Open modal</Button>

        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam
          euismod eget lorem in pharetra. Etiam iaculis vulputate lacus, at
          convallis ex interdum sed. Praesent laoreet, mauris porta interdum
          dictum, mauris dolor cursus enim, sit amet congue lectus leo vulputate
          ante. Nunc vitae ipsum dui. In finibus porttitor massa, et blandit
          augue tempor quis. Vestibulum imperdiet ipsum tellus. Sed ac consequat
          dolor. Nam purus eros, pretium quis vehicula et, fermentum commodo
          enim. Donec condimentum ipsum ut ex dignissim, a posuere enim
          pharetra.
        </p>

        <p>
          In condimentum luctus ultricies. Donec nec nulla eleifend, sodales
          nunc a, consectetur diam. Suspendisse ut enim pharetra, tempor dui
          nec, ornare mauris. Maecenas tincidunt ornare sapien vel posuere.
          Nullam dignissim dignissim sodales. Vivamus sit amet ligula ornare leo
          porttitor euismod sed porta magna. Vestibulum consectetur, elit id
          tristique varius, tortor orci condimentum nunc, in dignissim eros est
          at velit. Etiam in est pulvinar, interdum tortor id, venenatis elit.
          Aliquam ac faucibus lacus. Suspendisse blandit justo ex, ac dictum
          felis pellentesque sit amet.
        </p>

        <p>
          Morbi et hendrerit sem. Duis sollicitudin, nisi eget luctus pretium,
          risus enim porta turpis, vel ullamcorper nisi tortor at metus. Etiam
          dictum neque eu ipsum rhoncus, sed malesuada turpis rutrum. Nam
          lobortis lectus risus, at mollis velit fermentum et. Curabitur
          consectetur ornare leo nec euismod. Phasellus non libero vel arcu
          convallis dapibus. Donec ullamcorper condimentum nulla, accumsan
          scelerisque libero lacinia sed. Nunc tellus lorem, feugiat ac pretium
          sed, vulputate sed massa. Donec id urna eu urna semper elementum.
          Nullam et ligula vitae odio consectetur lobortis in varius lacus.
          Nullam pretium lectus quis augue vestibulum fringilla. Cras
          ullamcorper magna quis ex vestibulum, at sodales nulla bibendum. Sed
          varius lectus pulvinar maximus rutrum. Nulla suscipit, turpis vitae
          ultricies viverra, nunc lectus interdum lectus, eget rhoncus augue
          elit sed ante. Sed at nibh commodo, rhoncus erat eget, dictum nisi.
          Aliquam diam ligula, convallis nec leo in, auctor auctor magna.
        </p>

        <p>
          Vestibulum egestas odio tellus, ut pretium massa pharetra nec. Donec
          ut nulla et orci dignissim porttitor. Pellentesque habitant morbi
          tristique senectus et netus et malesuada fames ac turpis egestas.
          Pellentesque nibh est, facilisis ac congue quis, interdum ut leo.
          Donec posuere finibus ex, id euismod augue hendrerit non. Integer sit
          amet elementum elit. Sed congue sodales nisl ut aliquet. Vestibulum in
          ligula et turpis commodo tincidunt. Phasellus vitae elit purus. Aenean
          turpis elit, auctor eu velit eu, vestibulum bibendum orci. Nam
          imperdiet sodales sagittis.
        </p>

        <p>
          Proin interdum vitae libero et sollicitudin. Nullam ut rhoncus nunc.
          Integer magna odio, fermentum vitae euismod vitae, malesuada sed
          lorem. Sed lobortis id mi sed efficitur. Nulla facilisi. Donec egestas
          lectus in arcu interdum, id viverra mi feugiat. Nam tortor nibh,
          tristique ut aliquet quis, egestas vitae lectus. Etiam vel dui diam.
          Praesent dapibus vel purus nec tempor. Sed felis lectus, vehicula ut
          fermentum in, molestie id dolor. Pellentesque finibus, turpis non
          interdum auctor, velit nibh pulvinar nisl, vel tempor sapien enim in
          ante. Quisque in sapien feugiat, tincidunt enim et, mollis nunc.
          Aliquam auctor leo augue, et consequat diam feugiat et. Sed vulputate
          dictum libero, eget interdum orci auctor ac. Integer ac euismod risus.
          Nam placerat dapibus erat ut eleifend.
        </p>

        <p>
          Cras suscipit elit non faucibus facilisis. In hac habitasse platea
          dictumst. Donec sapien lorem, aliquet vel pretium non, egestas quis
          ligula. Aliquam erat volutpat. Duis diam elit, dapibus et varius
          vitae, ultricies rhoncus eros. Phasellus fermentum vel orci eu congue.
          Phasellus ac pellentesque urna. Vestibulum gravida est eget urna
          efficitur pulvinar eu ut lorem. Maecenas elit nunc, vestibulum sit
          amet orci tincidunt, hendrerit vulputate ante. Morbi quis sodales est.
        </p>

        <p>
          Donec suscipit, erat ac volutpat posuere, orci lorem consectetur quam,
          eget ultricies arcu nibh eu metus. Quisque massa nunc, viverra eu
          lobortis vitae, faucibus in enim. Fusce semper sed ligula id vehicula.
          Quisque eget urna leo. Interdum et malesuada fames ac ante ipsum
          primis in faucibus. Praesent faucibus nunc sed gravida rutrum. Donec
          vitae urna non dui malesuada lacinia. Morbi tincidunt mi vitae lectus
          suscipit, vitae tincidunt nisi egestas. Vivamus interdum orci et diam
          dictum, sed dignissim justo interdum. Etiam tempus aliquet nisl,
          ultricies dignissim tellus lacinia ac. Maecenas ullamcorper lacus ut
          sollicitudin dictum. Aenean a ligula sodales, tempus nibh vel,
          bibendum lorem.
        </p>

        <p>
          Vivamus sed orci molestie, rutrum velit nec, pulvinar erat. Sed at
          lectus porta massa euismod lacinia a a leo. Pellentesque leo leo,
          tempus ac molestie non, fringilla non massa. Aenean rhoncus pulvinar
          turpis quis scelerisque. Sed a tortor vulputate nisl vestibulum
          euismod. Aenean in arcu tempus, porttitor eros vel, efficitur nisi.
          Proin ut urna vel odio dapibus ultricies. Sed dui risus, dictum vel
          mauris sed, mollis cursus leo. Duis gravida, tellus varius aliquet
          vehicula, sapien mauris cursus tellus, non hendrerit augue justo id
          tortor. Ut dictum bibendum neque, vel interdum dui auctor id.
          Suspendisse tempor tortor quis accumsan vehicula. Mauris molestie
          sodales arcu, vitae euismod metus ornare id. Suspendisse vel nibh sed
          lectus sodales rutrum a et arcu.
        </p>

        <p>
          Integer tristique efficitur est, quis elementum diam venenatis nec.
          Suspendisse sollicitudin semper ipsum, id condimentum orci suscipit
          id. In placerat ipsum at lorem convallis, vitae porta tortor
          consequat. Proin mollis ipsum mauris, non dapibus dui auctor id. Sed
          placerat magna sit amet consequat volutpat. Fusce vitae ipsum eu lacus
          bibendum blandit. Aenean ullamcorper convallis lobortis. Donec
          vehicula porta nisl, et ultrices nisi rutrum ut. Phasellus condimentum
          risus est, eu imperdiet arcu molestie ac. Praesent imperdiet erat non
          dui maximus finibus. Curabitur a libero efficitur, congue libero in,
          placerat odio. Mauris risus velit, aliquet a justo vitae, lacinia
          iaculis sem. Aenean aliquet quam ac blandit faucibus. Nam ac lacus
          gravida turpis vehicula tempus. Sed rhoncus risus et est ullamcorper
          ultricies. Sed libero elit, tincidunt ut ipsum non, tempus condimentum
          nibh.
        </p>

        <p>
          Duis id eros id augue ultrices venenatis. Etiam elementum dolor non
          augue convallis, sit amet tincidunt tellus facilisis. Aenean odio
          lacus, scelerisque quis purus ut, tristique ultricies nunc. Fusce
          imperdiet sollicitudin sapien, vel ultrices arcu pharetra et. Sed
          molestie eget dui eu malesuada. Maecenas lacinia eros at turpis
          commodo, tincidunt vulputate mi imperdiet. Sed orci tortor, commodo ac
          euismod in, vestibulum at lectus. Quisque convallis sapien a placerat
          pulvinar. Sed in lorem et metus facilisis porta et eget massa.
          Pellentesque dignissim nisl sed quam bibendum sodales. Quisque in
          mauris cursus enim ullamcorper congue id aliquam ipsum. Praesent
          suscipit odio non turpis pretium porttitor. Vivamus fringilla nunc a
          placerat scelerisque. Nunc sed libero sollicitudin, lobortis felis
          eget, consequat velit. Mauris vel pretium lorem.{" "}
        </p>
      </div>

      {isModalOpen && (
        <Modal
          title="Modal"
          isOpen={isModalOpen}
          onDismiss={() => setIsModalOpen(false)}
        >
          <p>Modal content</p>
          <input
            placeholder="Type here"
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </Modal>
      )}
    </>
  );
}
